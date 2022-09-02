import xbmcgui
from resources.lib import utils, saved_stations


def directory_item(label, mode, **kwargs):
    list_item = xbmcgui.ListItem(label)
    query = {"mode": mode}
    query.update(kwargs)
    url = utils.build_url(query)
    return (url, list_item, True)


def next_page_item(response, mode, current_page, **kwargs):
    if len(response) == 50:
        list_item = xbmcgui.ListItem("Next Page")
        list_item.setInfo(
            "music", {"title": "Next Page", "genre": "Page %i" % (current_page + 2)}
        )
        query = {"mode": mode, "page": current_page + 1}
        query.update(kwargs)
        url = utils.build_url(query)
        return (url, list_item, True)


def station_item(station, number):
    resolved = isinstance(station, dict)

    if resolved:
        votes = ["[B]%i votes[/B]" % station["votes"]]

        language = station["language"].split(",")
        language = [i.title() for i in language]

        location = [station["state"], station["country"]]
        tags = station["tags"].split(",")

        cleaned_tags = [i for i in votes + language + location + tags if i]
        genre = ", ".join(cleaned_tags)

        if station["lastcheckok"] == 0:
            genre = "[B]Offline![/B] " + genre

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
            context_menu_items.append(
                (
                    "Add to Saved Stations",
                    "RunPlugin(%s)"
                    % utils.build_url(
                        {
                            "mode": "saved_station_add",
                            "uuid": station["stationuuid"],
                        }
                    ),
                )
            )
        else:
            context_menu_items.append(
                (
                    "Remove from Saved Stations",
                    "RunPlugin(%s)"
                    % utils.build_url(
                        {
                            "mode": "saved_station_remove",
                            "uuid": station["stationuuid"],
                        }
                    ),
                )
            )
        context_menu_items.append(
            (
                "Vote for Station",
                "RunPlugin(%s)"
                % utils.build_url({"mode": "vote", "uuid": station["stationuuid"]}),
            )
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
            context_menu_items.append(
                (
                    "Add to Saved Stations",
                    "RunPlugin(%s)"
                    % utils.build_url({"mode": "saved_station_add", "url": station}),
                )
            )
        else:
            context_menu_items.append(
                (
                    "Remove from Saved Stations",
                    "RunPlugin(%s)"
                    % utils.build_url({"mode": "saved_station_remove", "url": station}),
                )
            )
        url = utils.build_url({"mode": "listen", "url": station})

    list_item.addContextMenuItems(context_menu_items)
    return (url, list_item, False)


def sort_menu(mode, **kwargs):
    menu_list = []

    query = {"orderby": "votes", "reverse": "true"}
    query.update(kwargs)
    menu_list.append(directory_item("Most Voted First", mode, **query))

    query = {"orderby": "votes", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item("Least Voted First", mode, **query))

    query = {"orderby": "clickcount", "reverse": "true"}
    query.update(kwargs)
    menu_list.append(directory_item("Most Listeners First", mode, **query))

    query = {"orderby": "clickcount", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item("Least Listeners First", mode, **query))

    query = {"orderby": "name", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item("A-Z", mode, **query))

    query = {"orderby": "name", "reverse": "true"}
    query.update(kwargs)
    menu_list.append(directory_item("Z-A", mode, **query))

    query = {"orderby": "bitrate", "reverse": "true"}
    query.update(kwargs)
    menu_list.append(directory_item("Highest Bitrate First", mode, **query))

    query = {"orderby": "bitrate", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item("Lowest/Undefined Bitrate First", mode, **query))

    query = {"orderby": "changetimestamp", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item("Oldest Change First", mode, **query))

    query = {"orderby": "changetimestamp", "reverse": "true"}
    query.update(kwargs)
    menu_list.append(directory_item("Newest Change First", mode, **query))

    query = {"orderby": "random", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item("Random", mode, **query))

    return menu_list
