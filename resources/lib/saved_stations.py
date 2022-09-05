"""A module that stores functions for working with saved stations."""

import json
import os
from pathlib import Path

import xbmcgui
import xbmcvfs

from resources.lib import gui, server
from resources.lib.locale import localize_string as _

saved_stations = []
SAVED_STATIONS_PATH = xbmcvfs.translatePath(
    "special://profile/addon_data/plugin.audio.rbb/saved_stations.json"
)
Path(xbmcvfs.translatePath("special://profile/addon_data/plugin.audio.rbb")).mkdir(
    exist_ok=True
)


def update_saved_stations():
    """Writes the new saved stations to the JSON file."""
    with open(SAVED_STATIONS_PATH, "w+", encoding="utf-8") as file:
        json.dump(saved_stations, file)


def is_in_saved_stations(val: str, kind: str) -> bool:
    """
    Checks if a specified station is in the saved stations dict.

    Args:
        val (str): Station UUID or stream URL, depending on `kind`.
        kind (str): `"uuid"` or `"url"`.

    Returns:
        bool: `True` if the station is saved, else `False`.
    """
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
                    "JSON decode error occurred while loading saved stations, resetting stations..."
                ),
                str(e),
            )
            saved_stations_file.seek(0)
            saved_stations_file.write("[]")
            saved_stations_file.truncate()
            saved_stations = []


def get_saved_stations() -> list[tuple[str, xbmcgui.ListItem, bool]]:
    """
    Creates a list of saved stations to be used with `xbmcplugin.addDirectoryItems`.

    Returns:
        list[tuple[str, xbmcgui.ListItem, bool]]: The list of saved stations.
    """
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


def add_saved_station(val: str, kind: str):
    """
    Adds a new saved station and displays a notification.

    Args:
        val (str): Station UUID or stream URL, depending on `kind`.
        kind (str): `"uuid"` or `"url"`.
    """
    # TODO: add ability to name saved custom URL stations
    saved_stations.append({kind: val})
    update_saved_stations()
    xbmcgui.Dialog().notification(_("Station saved"), _("Saved successfully"))


def remove_saved_station(val: str, kind: str):
    """
    Removes a saved station and displays a notification.

    Args:
        val (str): Station UUID or stream URL, depending on `kind`.
        kind (str): `"uuid"` or `"url"`.
    """
    saved_stations.remove({kind: val})
    update_saved_stations()
    xbmcgui.Dialog().notification(_("Station removed"), _("Removed successfully"))
