import os
import sys
import json
from urllib.parse import urlencode
from pathlib import Path
import xbmcgui
import xbmcvfs
from resources.lib import server, gui


def build_url(query):
    base_url = sys.argv[0]
    return base_url + "?" + urlencode(query)


def get_saved_stations():
    path = xbmcvfs.translatePath(
        "special://profile/addon_data/plugin.audio.rbb/settings.json"
    )
    if not Path(path).is_file() or os.stat(path).st_size == 0:
        with open(path, "w+") as file:
            file.write("[]")
            return []
    with open(path, "r") as file:
        saved_stations = json.load(file)

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

        saved_stations = []
        for station in resolved_stations:
            saved_stations.append(gui.station_item(station, len(saved_stations) + 1))
        return saved_stations


def add_saved_station(val, kind):
    path = xbmcvfs.translatePath(
        "special://profile/addon_data/plugin.audio.rbb/settings.json"
    )
    with open(path, "r+") as file:
        try:
            saved_stations = json.load(file)
        except json.JSONDecodeError as e:
            saved_stations = []
        saved_stations.append({kind: val})
        file.seek(0)
        json.dump(saved_stations, file)
        xbmcgui.Dialog().notification("RadioBrowser²", "Station saved!")


def remove_saved_station(val, kind):
    path = xbmcvfs.translatePath(
        "special://profile/addon_data/plugin.audio.rbb/settings.json"
    )
    with open(path, "r+") as file:
        try:
            saved_stations = json.load(file)
        except json.JSONDecodeError:
            saved_stations = []
        saved_stations.remove({kind: val})
        file.seek(0)
        json.dump(saved_stations, file)
        xbmcgui.Dialog().notification("RadioBrowser²", "Station removed!")
