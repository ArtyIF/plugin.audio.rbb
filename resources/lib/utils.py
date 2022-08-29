import sys
from urllib.parse import urlencode
import xbmcgui


def build_url(query):
    base_url = sys.argv[0]
    return base_url + "?" + urlencode(query)


def next_page_item(response, mode, current_page, params={}):
    if len(response) == 50:
        # TODO: override the titlebar to indicate the page and kind if possible
        li = xbmcgui.ListItem(f"Next Page")
        li.setInfo("music", {"title": "Next Page", "genre": f"Page {current_page+2}"})
        query = {"mode": mode, "page": current_page + 1}
        query.update(params)
        url = build_url(query)
        return (url, li, True)


def station_item(station, number):
    votes = [f"[B]{station['votes']} votes[/B]"]
    # TODO: localize language and location. pycountry maybe?
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
    url = build_url(
        {
            "mode": "listen",
            "url": station["url_resolved"],
            "uuid": station["stationuuid"],
        }
    )
    return (url, li, False)


def sort_menu(mode, params={}):
    menu_list = []

    li = xbmcgui.ListItem("Most Voted First")
    query = {
        "mode": mode,
        "orderby": "votes",
        "reverse": "true",
    }
    query.update(params)
    url = build_url(query)
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Least Voted First")
    query = {
        "mode": mode,
        "orderby": "votes",
        "reverse": "false",
    }
    query.update(params)
    url = build_url(query)
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Most Listeners First")
    query = {
        "mode": mode,
        "orderby": "clickcount",
        "reverse": "true",
    }
    query.update(params)
    url = build_url(query)
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Least Listeners First")
    query = {
        "mode": mode,
        "orderby": "clickcount",
        "reverse": "false",
    }
    query.update(params)
    url = build_url(query)
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("A-Z")
    query = {
        "mode": mode,
        "orderby": "name",
        "reverse": "false",
    }
    query.update(params)
    url = build_url(query)
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Z-A")
    query = {
        "mode": mode,
        "orderby": "name",
        "reverse": "true",
    }
    query.update(params)
    url = build_url(query)
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Highest Bitrate First")
    query = {
        "mode": mode,
        "orderby": "bitrate",
        "reverse": "true",
    }
    query.update(params)
    url = build_url(query)
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Lowest/Undefined Bitrate First")
    query = {
        "mode": mode,
        "orderby": "bitrate",
        "reverse": "false",
    }
    query.update(params)
    url = build_url(query)
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Oldest Change First")
    query = {
        "mode": mode,
        "orderby": "changetimestamp",
        "reverse": "false",
    }
    query.update(params)
    url = build_url(query)
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Newest Change First")
    query = {
        "mode": mode,
        "orderby": "changetimestamp",
        "reverse": "true",
    }
    query.update(params)
    url = build_url(query)
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Random")
    query = {
        "mode": mode,
        "orderby": "random",
        "reverse": "false",
    }
    query.update(params)
    url = build_url(query)
    menu_list.append((url, li, True))

    return menu_list
