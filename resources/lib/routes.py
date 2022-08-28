import xbmc
import xbmcgui
import xbmcplugin

from resources.lib import server, utils


def root(addon_handle):
    menu_list = []

    li = xbmcgui.ListItem("Most Voted Stations")
    url = utils.build_url({"mode": "stations", "kind": "topvote"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Trending Stations")
    url = utils.build_url({"mode": "stations", "kind": "topclick"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations Recently Played by Others")
    url = utils.build_url({"mode": "stations", "kind": "lastclick"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Recently Added/Changed Stations")
    url = utils.build_url({"mode": "stations", "kind": "lastchange"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations by Country")
    url = utils.build_url({"mode": "countries"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations by State")
    url = utils.build_url({"mode": "state_countries"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations by State (A-Z)")
    url = utils.build_url({"mode": "states"})
    # menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations by Language")
    url = utils.build_url({"mode": "languages"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations by Tag")
    url = utils.build_url({"mode": "tags"})
    # menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Stations by Codec")
    url = utils.build_url({"mode": "codecs"})
    # menu_list.append((url, li, True))

    li = xbmcgui.ListItem("All Stations")
    url = utils.build_url({"mode": "stations", "kind": "all"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Favourites")
    url = utils.build_url({"mode": "favourites"})
    # menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Search by Name")
    url = utils.build_url({"mode": "search_by_name"})
    menu_list.append((url, li, True))

    li = xbmcgui.ListItem("Search by Tags")
    url = utils.build_url({"mode": "search_by_tags"})
    menu_list.append((url, li, True))

    xbmcplugin.addDirectoryItems(addon_handle, menu_list)
    xbmcplugin.endOfDirectory(addon_handle)


def get_stations(addon_handle, kind, page, orderby):
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
        language = [i.title() for i in language]

        location = [station["state"], station["country"]]
        tags = station["tags"].split(",")

        cleaned_tags = [i for i in language + location + tags if i]
        genre = ", ".join(cleaned_tags)

        if station["lastcheckok"] == 0:
            genre = "[B]Offline![/B] " + genre

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
                "poster": station["favicon"],
                "fanart": station["favicon"],
                "landscape": station["favicon"],
                "icon": station["favicon"],
            }
        )
        li.setProperty("IsPlayable", "true")
        url = utils.build_url(
            {"mode": "listen", "url": station["url"], "uuid": station["stationuuid"]}
        )
        station_list.append((url, li, False))

    station_list.append(
        utils.next_page_item(response, "stations", page, {"kind": kind})
    )
    station_list = [i for i in station_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, station_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def get_countries(addon_handle, page):
    page = int(page)
    response = server.get("/countries", {"offset": page * 50, "limit": 50}).json()

    countries_list = []
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
        url = utils.build_url(
            {"mode": "stations", "kind": "bycountrycodeexact/" + category["iso_3166_1"]}
        )
        countries_list.append((url, li, True))

    countries_list.append(utils.next_page_item(response, "countries", page))
    countries_list = [i for i in countries_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, countries_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def get_state_countries(addon_handle, page):
    page = int(page)
    response = server.get("/countries", {"offset": page * 50, "limit": 50}).json()

    state_countries_list = []
    for category in response:
        li = xbmcgui.ListItem(category["name"])

        li.setInfo(
            "music",
            {
                "title": category["name"],
                "genre": f"{category['stationcount']} total stations",  # TODO: replace with state count if possible
            },
        )
        url = utils.build_url({"mode": "states", "state": category["name"]})
        state_countries_list.append((url, li, True))

    state_countries_list.append(utils.next_page_item(response, "state_countries", page))
    state_countries_list = [i for i in state_countries_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, state_countries_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def get_states(addon_handle, state, page):
    page = int(page)
    response = server.get(
        f"/states/{state}/", {"offset": page * 50, "limit": 50}
    ).json()

    states_list = []
    for category in response:
        li = xbmcgui.ListItem(category["name"])

        li.setInfo(
            "music",
            {
                "title": category["name"],
                "genre": f"{category['stationcount']} stations",
            },
        )
        url = utils.build_url(
            # FIXME: sometimes it picks up similarly named states as well, like Bavaria, Germany when the user picked Bavaria, Netherlands
            {"mode": "stations", "kind": "bystateexact/" + category["name"]}
        )
        states_list.append((url, li, True))

    states_list.append(
        utils.next_page_item(response, "countries", page, {"state": state})
    )
    states_list = [i for i in states_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, states_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def get_languages(addon_handle, page):
    page = int(page)
    response = server.get("/languages", {"offset": page * 50, "limit": 50}).json()

    languages_list = []
    for category in response:
        li = xbmcgui.ListItem(category["name"].title())

        li.setInfo(
            "music",
            {
                "title": category["name"].title(),
                "genre": f"{category['stationcount']} stations",
            },
        )
        url = utils.build_url(
            {"mode": "stations", "kind": "bylanguageexact/" + category["name"]}
        )
        languages_list.append((url, li, True))

    languages_list.append(utils.next_page_item(response, "languages", page))
    languages_list = [i for i in languages_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, languages_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def get_tags(addon_handle, page):
    page = int(page)
    response = server.get("/tags", {"offset": page * 50, "limit": 50}).json()

    tags_list = []
    for category in response:
        li = xbmcgui.ListItem(category["name"])

        li.setInfo(
            "music",
            {
                "title": category["name"],
                "genre": f"{category['stationcount']} stations",
            },
        )
        url = utils.build_url(
            {"mode": "stations", "kind": "bytagexact/" + category["name"]}
        )
        tags_list.append((url, li, True))

    tags_list.append(utils.next_page_item(response, "tags", page))
    tags_list = [i for i in tags_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, tags_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def get_codecs(addon_handle, page):
    page = int(page)
    response = server.get("/codecs", {"offset": page * 50, "limit": 50}).json()

    codecs_list = []
    for category in response:
        li = xbmcgui.ListItem(category["name"])

        li.setInfo(
            "music",
            {
                "title": category["name"],
                "genre": f"{category['stationcount']} stations",
            },
        )
        url = utils.build_url(
            {"mode": "stations", "kind": "bycodecexact/" + category["name"]}
        )
        codecs_list.append((url, li, True))

    codecs_list.append(utils.next_page_item(response, "codecs", page))
    codecs_list = [i for i in codecs_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, codecs_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def perform_search(addon_handle, kind, search_text, page):
    page = int(page)
    response = server.get(
        "/stations/search", {kind: search_text, "offset": page * 50, "limit": 50}
    ).json()

    results_list = []
    for station in response:
        language = station["language"].split(",")
        language = [i.title() for i in language]

        location = [station["state"], station["country"]]
        tags = station["tags"].split(",")

        cleaned_tags = [i for i in language + location + tags if i]
        genre = ", ".join(cleaned_tags)

        if station["lastcheckok"] == 0:
            genre = "[B]Offline![/B] " + genre

        li = xbmcgui.ListItem(station["name"], genre)

        li.setInfo(
            "music",
            {
                "title": station["name"],
                "tracknumber": (page * 50) + len(results_list) + 1,
                "size": station["bitrate"],
                "genre": genre,
                "playcount": station["clickcount"],
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
            {"mode": "listen", "url": station["url"], "uuid": station["stationuuid"]}
        )
        results_list.append((url, li, False))

    results_list.append(
        utils.next_page_item(
            response, "results", page, {"kind": kind, "search_text": search_text}
        )
    )
    results_list = [i for i in results_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, results_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def open_search_by_name(addon_handle):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading("Enter the station name")
    keyboard.doModal()
    if keyboard.isConfirmed() and len(keyboard.getText()) > 0:
        perform_search(addon_handle, "name", keyboard.getText(), 0)


def open_search_by_tags(addon_handle):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading("Enter the comma-separated tags")
    keyboard.doModal()
    if keyboard.isConfirmed() and len(keyboard.getText()) > 0:
        perform_search(
            addon_handle,
            "tag",
            ",".join([i.strip() for i in keyboard.getText().split(",")]),
            0,
        )


def play(addon_handle, path, uuid):
    li = xbmcgui.ListItem(path=path)
    click_counter_result = server.post("/url/" + uuid).json()
    xbmcplugin.setResolvedUrl(addon_handle, click_counter_result.get("ok", False), li)
