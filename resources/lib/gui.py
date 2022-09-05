"""A module that stores common GUI functions."""

import xbmcgui

from resources.lib import saved_stations, utils
from resources.lib.locale import localize_string as _


def directory_item(
    label: str, mode: str, **kwargs: dict[str, str]
) -> tuple[str, xbmcgui.ListItem, bool]:
    """
    The directory item. Returns a `xbmcgui.ListItem` that goes to `mode`
    with `kwargs` as parameters when selected.

    Args:
        label (str): `ListItem`'s label shown to the user.
        mode (str): The mode that is passed to the plugin. Used to find a matching route.
        kwargs (dict[str, str]): The parameters passed to the plugin, then to the route.

    Returns:
        tuple[str, xbmcgui.ListItem, bool]: The tuple to be used with `xbmcgui.addDirectoryItems`.
    """
    list_item = xbmcgui.ListItem(label)
    query = {"mode": mode}
    query.update(kwargs)
    url = utils.build_url(query)
    return (url, list_item, True)


def next_page_item(
    response: str, mode: str, current_page: int, **kwargs: dict[str, str]
) -> tuple[str, xbmcgui.ListItem, bool] | None:
    """
    Creates an item that goes to the next page, if the list of stations is long enough.

    Args:
        response (str): The list of stations. Used to determine if this option is even necessary.
        mode (str): The mode that is passed to the plugin. Used to find a matching route.
        current_page (int): The current page number, 0 being the first one.
        kwargs (dict[str, str]): The parameters passed to the plugin, then to the route.

    Returns:
        tuple[str, xbmcgui.ListItem, bool]: The tuple to be used with `xbmcgui.addDirectoryItems`.
    """
    if len(response) == 50:
        list_item = xbmcgui.ListItem(_("Next page"))
        list_item.setInfo(
            "music",
            {"title": _("Next page"), "genre": _("Page {0}").format(current_page + 2)},
        )
        query = {"mode": mode, "page": current_page + 1}
        query.update(kwargs)
        url = utils.build_url(query)
        return (url, list_item, True)


def station_item(
    station: dict | str, number: str
) -> tuple[str, xbmcgui.ListItem, bool]:
    """
    Creates a list item that represents a station.

    Args:
        station (dict | str): The station dict or URL
        number (str): The station's track number.

    Returns:
        tuple[str, xbmcgui.ListItem, bool]: The tuple to be used with `xbmcgui.addDirectoryItems`.
    """
    resolved = isinstance(station, dict)

    if resolved:
        votes = [_("[B]{0} votes[/B]").format(station["votes"])]

        # TODO: localize language
        language = station["language"].split(",")
        language = [i.title() for i in language]

        # TODO: localize state and country
        location = [station["state"], station["country"]]
        tags = station["tags"].split(",")

        cleaned_tags = [i for i in votes + language + location + tags if i]
        genre = ", ".join(cleaned_tags)

        if station["lastcheckok"] == 0:
            genre = _("[B]Offline![/B]") + " " + genre

        list_item = xbmcgui.ListItem(station["name"], genre)
    else:
        genre = ""
        list_item = xbmcgui.ListItem(station, genre)

    if resolved:
        list_item.setInfo(
            "music",
            {
                "title": station["name"],
                "tracknumber": number,
                "size": station["bitrate"],
                "genre": genre,
            },
        )
        list_item.setArt(
            {
                "thumb": station["favicon"],
                "poster": station["favicon"],
                "fanart": station["favicon"],
                "landscape": station["favicon"],
                "icon": station["favicon"],
            }
        )
    else:
        list_item.setInfo("music", {"title": station})

    list_item.setProperty("IsPlayable", "true")

    context_menu_items = []
    if resolved:
        if not saved_stations.is_in_saved_stations(station["stationuuid"], "uuid"):
            saved_stations_url = utils.build_url(
                {"mode": "saved_station_add", "uuid": station["stationuuid"]}
            )
            context_menu_items.append(
                (_("Add to saved stations"), f"RunPlugin({saved_stations_url})")
            )
        else:
            saved_stations_url = utils.build_url(
                {"mode": "saved_station_remove", "uuid": station["stationuuid"]}
            )
            context_menu_items.append(
                (_("Remove from saved stations"), f"RunPlugin({saved_stations_url})")
            )

        vote_for_station_url = utils.build_url(
            {"mode": "vote", "uuid": station["stationuuid"]}
        )
        context_menu_items.append(
            (_("Vote for station"), f"RunPlugin({vote_for_station_url})")
        )

        url = utils.build_url(
            {
                "mode": "listen",
                "url": station["url_resolved"],
                "uuid": station["stationuuid"],
            }
        )
    else:
        if not saved_stations.is_in_saved_stations(station, "url"):
            saved_stations_url = utils.build_url(
                {"mode": "saved_station_add", "url": station}
            )
            context_menu_items.append(
                (_("Add to saved stations"), f"RunPlugin({saved_stations_url})")
            )
        else:
            saved_stations_url = utils.build_url(
                {"mode": "saved_station_remove", "url": station}
            )
            context_menu_items.append(
                (_("Remove from saved stations"), f"RunPlugin({saved_stations_url})")
            )
        url = utils.build_url({"mode": "listen", "url": station})

    list_item.addContextMenuItems(context_menu_items)
    return (url, list_item, False)


def sort_menu(
    mode: str, **kwargs: dict[str, str]
) -> list[tuple[str, xbmcgui.ListItem, bool]]:
    """
    Creates a menu to sort list items (usually stations) by:
    * votes
    * listeners
    * alphabetically
    * bitrate
    * change
    * randomly

    The sorting is done on the server's side by passing the `orderby` and
    `reverse` parameters to the query.

    Args:
        mode (str): The mode that is passed to the plugin. Used to find a matching route.
        kwargs (dict[str, str]): The parameters passed to the plugin, then to the route.

    Returns:
        list[tuple[str, xbmcgui.ListItem, bool]]: A list to be passed to
        `xbmcgui.addDirectoryItems`.
    """
    menu_list = []

    query = {"orderby": "votes", "reverse": "true"}
    query.update(kwargs)
    menu_list.append(directory_item(_("Most voted first"), mode, **query))

    query = {"orderby": "votes", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item(_("Least voted first"), mode, **query))

    query = {"orderby": "clickcount", "reverse": "true"}
    query.update(kwargs)
    menu_list.append(directory_item(_("Most listeners first"), mode, **query))

    query = {"orderby": "clickcount", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item(_("Least listeners first"), mode, **query))

    query = {"orderby": "name", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item(_("A-Z"), mode, **query))

    query = {"orderby": "name", "reverse": "true"}
    query.update(kwargs)
    menu_list.append(directory_item(_("Z-A"), mode, **query))

    query = {"orderby": "bitrate", "reverse": "true"}
    query.update(kwargs)
    menu_list.append(directory_item(_("Highest bitrate first"), mode, **query))

    query = {"orderby": "bitrate", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item(_("Lowest/undefined bitrate first"), mode, **query))

    query = {"orderby": "changetimestamp", "reverse": "true"}
    query.update(kwargs)
    menu_list.append(directory_item(_("Newest change first"), mode, **query))

    query = {"orderby": "changetimestamp", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item(_("Oldest change first"), mode, **query))

    query = {"orderby": "random", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item(_("Random"), mode, **query))

    return menu_list
