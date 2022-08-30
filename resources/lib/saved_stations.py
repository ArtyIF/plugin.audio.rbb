import os
from pathlib import Path
import xbmcgui
import xbmcvfs
import json
from resources.lib import server, gui


saved_stations = []
saved_stations_path = xbmcvfs.translatePath(
    "special://profile/addon_data/plugin.audio.rbb/settings.json"
)


def update_saved_stations():
    global saved_stations, saved_stations_path
    with open(saved_stations_path, "w+") as file:
        json.dump(saved_stations, file)


def is_in_saved_stations(val, kind):
    global saved_stations
    return {kind: val} in saved_stations


if not Path(saved_stations_path).is_file() or os.stat(saved_stations_path).st_size == 0:
    saved_stations = []
    update_saved_stations()
else:
    with open(saved_stations_path, "r+") as file:
        try:
            saved_stations = json.load(file)
        except json.JSONDecodeError as e:
            # TODO: backup instead of deleting
            xbmcgui.Dialog().notification(
                "JSON decode error occured when loading saved stations, resetting saved stations...",
                str(e),
            )
            file.seek(0)
            file.write("[]")
            file.truncate()
            saved_stations = []


def get_saved_stations():
    global saved_stations

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
        station_items.append(gui.station_item(station, len(saved_stations) + 1))
    return station_items


def add_saved_station(val, kind):
    global saved_stations

    # TODO: add ability to name saved custom URL stations
    saved_stations.append({kind: val})
    update_saved_stations()
    xbmcgui.Dialog().notification("RadioBrowser²", "Station saved!")


def remove_saved_station(val, kind):
    global saved_stations

    saved_stations.remove({kind: val})
    update_saved_stations()
    xbmcgui.Dialog().notification("RadioBrowser²", "Station removed!")
