import xbmcgui
from resources.lib import utils


def directory_item(label, mode, **kwargs):
    li = xbmcgui.ListItem(label)
    query = {"mode": mode}
    query.update(kwargs)
    url = utils.build_url(query)
    return (url, li, True)


def next_page_item(response, mode, current_page, **kwargs):
    if len(response) == 50:
        li = xbmcgui.ListItem(f"Next Page")
        li.setInfo("music", {"title": "Next Page", "genre": f"Page {current_page+2}"})
        query = {"mode": mode, "page": current_page + 1}
        query.update(kwargs)
        url = utils.build_url(query)
        return (url, li, True)


def station_item(station, number):
    votes = [f"[B]{station['votes']} votes[/B]"]

    language = station["language"].split(",")
    language = [i.title() for i in language]

    location = [station["state"], station["country"]]
    tags = station["tags"].split(",")

    cleaned_tags = [i for i in votes + language + location + tags if i]
    genre = ", ".join(cleaned_tags)

    if station["lastcheckok"] == 0:
        genre = "[B]Offline![/B] " + genre

    li = xbmcgui.ListItem(station["name"], genre)

    li.setInfo(
        "music",
        {
            "title": station["name"],
            "tracknumber": number,
            "size": station["bitrate"],
            "genre": genre,
        },
    )
    li.setArt(
        {
            "thumb": station["favicon"],
            "poster": station["favicon"],
            "fanart": station["favicon"],
            "landscape": station["favicon"],
            "icon": station["favicon"],
        }
    )
    li.setProperty("IsPlayable", "true")
    url = utils.build_url(
        {
            "mode": "listen",
            "url": station["url_resolved"],
            "uuid": station["stationuuid"],
        }
    )
    return (url, li, False)


def sort_menu(mode, **kwargs):
    menu_list = []

    query = {"orderby": "votes", "reverse": "true"}
    query.update(kwargs)
    menu_list.append(directory_item("Most Voted First", mode, query))

    query = {"orderby": "votes", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item("Least Voted First", mode, query))

    query = {"orderby": "clickcount", "reverse": "true"}
    query.update(kwargs)
    menu_list.append(directory_item("Most Listeners First", mode, query))

    query = {"orderby": "clickcount", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item("Least Listeners First", mode, query))

    query = {"orderby": "name", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item("A-Z", mode, query))

    query = {"orderby": "name", "reverse": "true"}
    query.update(kwargs)
    menu_list.append(directory_item("Z-A", mode, query))

    query = {"orderby": "bitrate", "reverse": "true"}
    query.update(kwargs)
    menu_list.append(directory_item("Highest Bitrate First", mode, query))

    query = {"orderby": "bitrate", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item("Lowest/Undefined Bitrate First", mode, query))

    query = {"orderby": "changetimestamp", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item("Oldest Change First", mode, query))

    query = {"orderby": "changetimestamp", "reverse": "true"}
    query.update(kwargs)
    menu_list.append(directory_item("Newest Change First", mode, query))

    query = {"orderby": "random", "reverse": "false"}
    query.update(kwargs)
    menu_list.append(directory_item("Random", mode, query))

    return menu_list
