import os
import json
from pathlib import Path
import xbmcgui
import xbmcvfs

from resources.lib import server, gui
from resources.lib.locale import localize_string as _


saved_stations = []
SAVED_STATIONS_PATH = xbmcvfs.translatePath(
    "special://profile/addon_data/plugin.audio.rbb/saved_stations.json"
)
Path(xbmcvfs.translatePath("special://profile/addon_data/plugin.audio.rbb")).mkdir(
    exist_ok=True
)


def update_saved_stations():
    with open(SAVED_STATIONS_PATH, "w+", encoding="utf-8") as file:
        json.dump(saved_stations, file)


def is_in_saved_stations(val, kind):
    return {kind: val} in saved_stations


if not Path(SAVED_STATIONS_PATH).is_file() or os.stat(SAVED_STATIONS_PATH).st_size == 0:
    saved_stations = []
    update_saved_stations()
else:
    with open(SAVED_STATIONS_PATH, "r+", encoding="utf-8") as saved_stations_file:
        try:
            saved_stations = json.load(saved_stations_file)
        except json.JSONDecodeError as e:
            # TODO: backup instead of deleting
            xbmcgui.Dialog().notification(
                _(
                    "JSON decode error occured while loading saved stations, resetting stations..."
                ),
                str(e),
            )
            saved_stations_file.seek(0)
            saved_stations_file.write("[]")
            saved_stations_file.truncate()
            saved_stations = []


def get_saved_stations():
    resolved_stations = []
    if len(saved_stations) > 0:
        saved_station_uuids = []
        for saved_station in saved_stations:
            if saved_station.get("uuid", None):
                saved_station_uuids.append(saved_station["uuid"])
        server.connect()
        response = server.get(
            "/stations/byuuid", {"uuids": ",".join(saved_station_uuids)}
        ).json()
        resolved_stations += response
        for saved_station in saved_stations:
            if saved_station.get("url", None):
                resolved_stations.append(saved_station["url"])

    station_items = []
    for station in resolved_stations:
        station_items.append(gui.station_item(station, len(station_items) + 1))
    return station_items


def add_saved_station(val, kind):
    # TODO: add ability to name saved custom URL stations
    saved_stations.append({kind: val})
    update_saved_stations()
    xbmcgui.Dialog().notification(_("Station saved!"), _("Saved successfully"))


def remove_saved_station(val, kind):
    saved_stations.remove({kind: val})
    update_saved_stations()
    xbmcgui.Dialog().notification(_("Station removed!"), _("Removed successfully"))
