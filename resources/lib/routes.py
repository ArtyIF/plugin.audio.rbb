import xbmc
import xbmcgui
import xbmcplugin

from resources.lib import server, utils, gui


def root(addon_handle):
    menu_list = []
    # menu_list.append(gui.directory_item("Favourites", "favourites"))
    menu_list.append(gui.directory_item("Most Voted Stations", "stations", kind="topvote"))
    menu_list.append(gui.directory_item("Trending Stations", "stations", kind="topclick"))
    menu_list.append(
        gui.directory_item(
            "Stations Recently Played by Others", "stations", kind="lastclick"
        )
    )
    menu_list.append(
        gui.directory_item(
            "Recently Added/Changed Stations", "stations", kind="lastchange"
        )
    )
    menu_list.append(gui.directory_item("Stations by...", "stations_by"))
    menu_list.append(gui.directory_item("Search...", "search"))

    xbmcplugin.addDirectoryItems(addon_handle, menu_list)
    xbmcplugin.endOfDirectory(addon_handle)


def get_stations(addon_handle, kind, page, orderby, reverse):
    page = int(page)
    request_url = f"/stations/{kind}"
    if kind == "all":
        request_url = "/stations"
    response = server.get(
        request_url,
        {"offset": page * 50, "limit": 50, "order": orderby, "reverse": reverse},
    ).json()

    station_list = []
    for station in response:
        station_list.append(
            gui.station_item(station, (page * 50) + len(station_list) + 1)
        )

    station_list.append(gui.next_page_item(response, "stations", page, kind=kind))
    station_list = [i for i in station_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, station_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def open_stations_directory(addon_handle):
    menu_list = []
    menu_list.append(gui.directory_item("Stations by Country", "countries"))
    menu_list.append(gui.directory_item("Stations by State", "state_countries"))
    menu_list.append(gui.directory_item("Stations by Language", "languages"))
    menu_list.append(gui.directory_item("Stations by Tag", "tags"))
    menu_list.append(gui.directory_item("Stations by Codec", "codecs"))
    menu_list.append(gui.directory_item("All Stations", "stations_sort", kind="all"))

    xbmcplugin.addDirectoryItems(addon_handle, menu_list)
    xbmcplugin.endOfDirectory(addon_handle)


def open_search_directory(addon_handle):
    menu_list = []
    menu_list.append(gui.directory_item("Search by Name", "search_by_name"))
    menu_list.append(gui.directory_item("Search by Tags", "search_by_tags"))

    xbmcplugin.addDirectoryItems(addon_handle, menu_list)
    xbmcplugin.endOfDirectory(addon_handle)


def open_stations_sort_directory(addon_handle, kind):
    menu_list = gui.sort_menu("stations", kind=kind)
    xbmcplugin.addDirectoryItems(addon_handle, menu_list)
    xbmcplugin.endOfDirectory(addon_handle)


def open_search_sort_directory(addon_handle, kind, search_text):
    menu_list = gui.sort_menu("results", kind=kind, search_text=search_text)
    xbmcplugin.addDirectoryItems(addon_handle, menu_list)
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
            {
                "mode": "stations_sort",
                "kind": "bycountrycodeexact/" + category["iso_3166_1"],
            }
        )
        countries_list.append((url, li, True))

    countries_list.append(gui.next_page_item(response, "countries", page))
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

    state_countries_list.append(gui.next_page_item(response, "state_countries", page))
    state_countries_list = [i for i in state_countries_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, state_countries_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def get_states(addon_handle, state, page):
    page = int(page)
    response = server.get(
        f"/states/{state}/",
        {
            "offset": page * 50,
            "limit": 50,
            "order": "stationcount",
            "reverse": "true",
        },
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
            {"mode": "stations_sort", "kind": "bystateexact/" + category["name"]}
        )
        states_list.append((url, li, True))

    states_list.append(gui.next_page_item(response, "countries", page, state=state))
    states_list = [i for i in states_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, states_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def get_languages(addon_handle, page):
    page = int(page)
    response = server.get(
        "/languages",
        {
            "offset": page * 50,
            "limit": 50,
            "order": "stationcount",
            "reverse": "true",
        },
    ).json()

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
            {"mode": "stations_sort", "kind": "bylanguageexact/" + category["name"]}
        )
        languages_list.append((url, li, True))

    languages_list.append(gui.next_page_item(response, "languages", page))
    languages_list = [i for i in languages_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, languages_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def get_tags(addon_handle, page):
    page = int(page)
    response = server.get(
        "/tags",
        {
            "offset": page * 50,
            "limit": 50,
            "order": "stationcount",
            "reverse": "true",
        },
    ).json()

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
            {"mode": "stations_sort", "kind": "bytagexact/" + category["name"]}
        )
        tags_list.append((url, li, True))

    tags_list.append(gui.next_page_item(response, "tags", page))
    tags_list = [i for i in tags_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, tags_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def get_codecs(addon_handle, page):
    page = int(page)
    response = server.get(
        "/codecs",
        {
            "offset": page * 50,
            "limit": 50,
            "order": "stationcount",
            "reverse": "true",
        },
    ).json()

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
            {"mode": "stations_sort", "kind": "bycodecexact/" + category["name"]}
        )
        codecs_list.append((url, li, True))

    codecs_list.append(gui.next_page_item(response, "codecs", page))
    codecs_list = [i for i in codecs_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, codecs_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def perform_search(addon_handle, kind, search_text, orderby, reverse, page):
    page = int(page)
    response = server.get(
        "/stations/search",
        {
            kind: search_text,
            "offset": page * 50,
            "limit": 50,
            "order": orderby,
            "reverse": reverse,
        },
    ).json()

    results_list = []
    for station in response:
        results_list.append(
            gui.station_item(station, (page * 50) + len(results_list) + 1)
        )

    results_list.append(
        gui.next_page_item(
            response, "results", page, kind=kind, search_text=search_text
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
        open_search_sort_directory(addon_handle, "name", keyboard.getText())


def open_search_by_tags(addon_handle):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading("Enter the comma-separated tags")
    keyboard.doModal()
    if keyboard.isConfirmed() and len(keyboard.getText()) > 0:
        open_search_sort_directory(
            addon_handle,
            "tag",
            ",".join([i.strip() for i in keyboard.getText().split(",")]),
        )


def play(addon_handle, path, uuid):
    li = xbmcgui.ListItem(path=path)
    click_counter_result = server.post("/url/" + uuid).json()
    xbmcplugin.setResolvedUrl(addon_handle, click_counter_result.get("ok", False), li)
