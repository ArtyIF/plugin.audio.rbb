import os
import sys
import xbmcaddon
import xbmcgui
import xbmcplugin
from datetime import datetime
from urllib.parse import urlencode, parse_qs

from resources.lib import server


def build_url(query):
    base_url = sys.argv[0]
    return base_url + "?" + urlencode(query)


def root():
    menu_list = []

    li = xbmcgui.ListItem("Most Voted Stations")
    url = build_url({"mode": "stations", "kind": "topvote"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Trending Stations")
    url = build_url({"mode": "stations", "kind": "topclick"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations Recently Played by Others")
    url = build_url({"mode": "stations", "kind": "lastclick"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Recently Added/Changed Stations")
    url = build_url({"mode": "stations", "kind": "lastchange"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations by Country")
    url = build_url({"mode": "categories", "ls": "countries", "kind": "bycountry"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations by State")
    url = build_url({"mode": "categories", "ls": "states", "kind": "bystate"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations by Language")
    url = build_url({"mode": "categories", "ls": "languages", "kind": "bylanguage"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations by Tag")
    url = build_url({"mode": "categories", "ls": "tags", "kind": "bytag"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations by Codec")
    url = build_url({"mode": "categories", "ls": "codecs", "kind": "bycodec"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("All Stations")
    url = build_url({"mode": "stations", "kind": "all"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Favourites")
    url = build_url({"mode": "favourites"})
    # menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Search")
    url = build_url({"mode": "search"})
    # menu_list.append((url, li, True))

    xbmcplugin.addDirectoryItems(addon_handle, menu_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def get_stations(kind, page, orderby):
    page = int(page)
    request_url = f"/stations/{kind}"
    if kind == "all":
        request_url = "/stations"
    response = server.get(
        request_url, {"offset": page * 50, "limit": 50, "order": orderby}
    ).json()

    station_list = []
    for station in response:
        # TODO: localize language and location. pycountry maybe?
        language = station["language"].split(",")
        location = [station["state"], station["country"]]
        tags = station["tags"].split(",")
        cleaned_tags = [i for i in language + location + tags if i]
        genre = ", ".join(cleaned_tags)
        li = xbmcgui.ListItem(station["name"], genre)

        li.setInfo(
            "music",
            {
                "title": station["name"],
                "tracknumber": (page * 50) + len(station_list) + 1,
                "size": station["bitrate"],
                "genre": genre,
                "playcount": station["clickcount"],
            },
        )
        li.setArt(
            {
                "thumb": station["favicon"],
                "fanart": station["favicon"],
                "icon": station["favicon"],
            }
        )
        li.setProperty("IsPlayable", "true")
        url = build_url(
            {"mode": "listen", "url": station["url"], "uuid": station["stationuuid"]}
        )
        station_list.append((url, li, False))

    if len(response) == 50:
        # TODO: override the titlebar to indicate the page and kind if possible
        li = xbmcgui.ListItem(f"Next Page")
        li.setInfo("music", {"title": "Next Page", "genre": f"Page {page+2}"})
        url = build_url({"mode": "stations", "kind": kind, "page": page + 1})
        station_list.append((url, li, True))
    xbmcplugin.addDirectoryItems(addon_handle, station_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def get_categories(ls, kind, page):
    page = int(page)
    response = server.get("/" + ls, {"offset": page * 50, "limit": 50}).json()

    categories_list = []
    for category in response:
        li = xbmcgui.ListItem(category["name"])

        li.setInfo(
            "music",
            {
                "title": category["name"],
                "count": category["stationcount"],
                "genre": f"{category['stationcount']} stations",
            },
        )
        url = build_url({"mode": "stations", "kind": kind + "/" + category["name"]})
        categories_list.append((url, li, True))

    if len(response) == 50:
        # TODO: override the titlebar to indicate the page and kind if possible
        li = xbmcgui.ListItem(f"Next Page")
        li.setInfo("music", {"title": "Next Page", "genre": f"Page {page+2}"})
        url = build_url(
            {"mode": "categories", "ls": ls, "kind": kind, "page": page + 1}
        )
        categories_list.append((url, li, True))
    xbmcplugin.addDirectoryItems(addon_handle, categories_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def play(path, uuid):
    li = xbmcgui.ListItem(path=path)
    click_counter_result = server.post("/url/" + uuid).json()
    xbmcplugin.setResolvedUrl(addon_handle, click_counter_result.get("ok", False), li)


def main():
    args = parse_qs(sys.argv[2][1:])
    mode = args.get("mode", None)

    # initial launch of add-on
    if mode is None:
        root()
    elif mode[0] == "stations":
        get_stations(
            args["kind"][0], args.get("page", [0])[0], args.get("orderby", ["name"])[0]
        )
    elif mode[0] == "categories":
        get_categories(args["ls"][0], args["kind"][0], args.get("page", [0])[0])
    elif mode[0] == "listen":
        play(args["url"][0], args["uuid"][0])

if __name__ == "__main__":
    server.connect()
    addon_handle = int(sys.argv[1])
    main()
