from json import JSONDecodeError
import os
import sys
import xbmcaddon
import xbmcgui
import xbmcplugin
from datetime import datetime

import socket
import random
import requests
from urllib.parse import urlencode, parse_qs

headers = {"User-Agent": "RadioBrowser2/0.1.0"}

# from https://api.radio-browser.info/examples/serverlist_python3.py
def get_radiobrowser_base_urls():
    hosts = []
    ips = socket.getaddrinfo("all.api.radio-browser.info", 80, 0, 0, socket.IPPROTO_TCP)
    for ip_tuple in ips:
        ip = ip_tuple[4][0]

        host_addr = socket.gethostbyaddr(ip)
        if host_addr[0] not in hosts:
            hosts.append(host_addr[0])

    hosts.sort()
    return hosts


def get_appropriate_server():
    # TODO: if you remove the return below it will repeatedly try to connect to that server, after which it'll raise an exception
    # TODO: enable connecting to other servers
    return "de1.api.radio-browser.info"
    servers = get_radiobrowser_base_urls()
    for server_base in servers:
        uri = f"https://{server_base}/json/stats"

        try:
            data = requests.get(uri, headers=headers)
            if data.status_code == 200:
                return server_base
            else:
                raise ConnectionError(
                    f"requests.get({uri}) returned status code {data.status_code}"
                )
        except ConnectionError:
            continue
    raise ConnectionError("Could not connect to any of radio-browser.info servers")


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
    url = build_url({"mode": "categories", "kind": "countries"})
    #menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations by State")
    url = build_url({"mode": "categories", "kind": "state"})
    #menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations by Language")
    url = build_url({"mode": "categories", "kind": "languages"})
    #menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations by Tag")
    url = build_url({"mode": "categories", "kind": "tags"})
    #menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations by Codec")
    url = build_url({"mode": "categories", "kind": "codecs"})
    #menu_list.append((url, li, True))

    li = xbmcgui.ListItem("All Stations")
    url = build_url({"mode": "stations", "kind": "all"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Favourites")
    url = build_url({"mode": "favourites"})
    #menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Search")
    url = build_url({"mode": "search"})
    #menu_list.append((url, li, True))

    xbmcplugin.addDirectoryItems(addon_handle, menu_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def get_station_list(kind, page):
    page = int(page)
    request_url = server_url + f"/stations/{kind}"
    if kind == "all":
        request_url = server_url + "/stations"
    response = requests.get(
        request_url, headers=headers, params={"offset": page * 50, "limit": 50}
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
                "date": datetime.fromisoformat(
                    station["lastcheckoktime_iso8601"].replace("Z", "+00:00")
                ).strftime("%d.%m.%Y"),
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
        li = xbmcgui.ListItem(f"Next (Page {page+2})")
        url = build_url({"mode": "stations", "kind": kind, "page": page + 1})
        station_list.append((url, li, True))
    xbmcplugin.addDirectoryItems(addon_handle, station_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def play(path, uuid):
    li = xbmcgui.ListItem(path=path)
    click_counter_result = requests.get(
        server_url + "/url/" + uuid, headers=headers
    ).json()
    xbmcplugin.setResolvedUrl(addon_handle, click_counter_result.get("ok", False), li)


def main():
    args = parse_qs(sys.argv[2][1:])
    mode = args.get("mode", None)

    # initial launch of add-on
    if mode is None:
        root()
    elif mode[0] == "stations":
        get_station_list(args["kind"][0], args.get("page", [0])[0])
    elif mode[0] == "listen":
        play(args["url"][0], args["uuid"][0])


if __name__ == "__main__":
    server_name = get_appropriate_server()
    server_url = f"https://{server_name}/json"
    addon_handle = int(sys.argv[1])
    main()
