import os
import sys
import json
from urllib.parse import urlencode
from pathlib import Path
import xbmcvfs
from resources.lib import server, gui


def build_url(query):
    base_url = sys.argv[0]
    return base_url + "?" + urlencode(query)


def get_favourites():
    path = xbmcvfs.translatePath(
        "special://profile/addon_data/plugin.audio.rbb/settings.json"
    )
    if not Path(path).is_file() or os.stat(path).st_size == 0:
        with open(path, "w+") as file:
            file.write("[]")
            return []
    with open(path, "r") as file:
        favourite_uuids = json.load(file)

        if len(favourite_uuids) > 0:
            server.connect()
            response = server.get(
                "/stations/byuuid/" + ",".join(favourite_uuids)
            ).json()
        else:
            response = []

        favourites = []
        for station in response:
            favourites.append(gui.station_item(station, len(favourites) + 1))
        return favourites


def add_favourite(val, kind="uuid"):
    path = xbmcvfs.translatePath(
        "special://profile/addon_data/plugin.audio.rbb/settings.json"
    )
    if not Path(path).is_file() or os.stat(path).st_size == 0:
        with open(path, "w+") as file:
            file.write("[]")
            return []
    with open(path, "r") as file:
        favourites = json.load(file)
        favourites.append({kind: val})
        json.dump(favourites, file)


def remove_favourite(val, kind="uuid"):
    path = xbmcvfs.translatePath(
        "special://profile/addon_data/plugin.audio.rbb/settings.json"
    )
    if not Path(path).is_file() or os.stat(path).st_size == 0:
        with open(path, "w+") as file:
            file.write("[]")
            return []
    with open(path, "r") as file:
        favourites = json.load(file)
        favourites.remove({kind: val})
        json.dump(favourites, file)
