import xbmc
import xbmcgui
import xbmcplugin

from resources.lib import server, utils, gui, saved_stations
from resources.lib.locale import localize_string as _


def root(addon_handle):
    menu_list = []
    menu_list.append(gui.directory_item(_("Saved Stations"), "saved_stations"))
    menu_list.append(
        gui.directory_item(_("Most Voted Stations"), "stations", kind="topvote")
    )
    menu_list.append(
        gui.directory_item(_("Trending Stations"), "stations", kind="topclick")
    )
    menu_list.append(
        gui.directory_item(
            _("Stations Recently Played by Others"), "stations", kind="lastclick"
        )
    )
    menu_list.append(
        gui.directory_item(
            _("Recently Added/Changed Stations"), "stations", kind="lastchange"
        )
    )
    menu_list.append(gui.directory_item(_("Stations by..."), "stations_by"))
    menu_list.append(gui.directory_item(_("Search..."), "search"))
    menu_list.append(gui.directory_item(_("Custom URL"), "custom_url"))

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

    station_list.append(
        gui.next_page_item(
            response,
            "stations",
            page,
            kind=kind,
            orderby=orderby,
            reverse=reverse,
        )
    )
    station_list = [i for i in station_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, station_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def open_stations_directory(addon_handle):
    menu_list = []
    menu_list.append(gui.directory_item(_("Stations by Country"), "countries"))
    menu_list.append(gui.directory_item(_("Stations by State"), "state_countries"))
    menu_list.append(gui.directory_item(_("Stations by Language"), "languages"))
    menu_list.append(gui.directory_item(_("Stations by Tag"), "tags"))
    menu_list.append(gui.directory_item(_("Stations by Codec"), "codecs"))
    menu_list.append(gui.directory_item(_("All Stations"), "stations_sort", kind="all"))

    xbmcplugin.addDirectoryItems(addon_handle, menu_list)
    xbmcplugin.endOfDirectory(addon_handle)


def open_search_directory(addon_handle):
    menu_list = []
    menu_list.append(gui.directory_item(_("Search by Name"), "search_by_name"))
    menu_list.append(gui.directory_item(_("Search by Tags"), "search_by_tags"))

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
        list_item = xbmcgui.ListItem(category["name"])

        list_item.setInfo(
            "music",
            {
                "title": category["name"],
                "count": category["stationcount"],
                "genre": _("{0} stations").format(category["stationcount"]),
            },
        )
        url = utils.build_url(
            {
                "mode": "stations_sort",
                "kind": "bycountrycodeexact/" + category["iso_3166_1"],
            }
        )
        countries_list.append((url, list_item, True))

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
        list_item = xbmcgui.ListItem(category["name"])

        list_item.setInfo(
            "music",
            {
                "title": category["name"],
                "genre": _("{0} total stations").format(
                    category["stationcount"]
                ),  # TODO: replace with state count if possible
            },
        )
        url = utils.build_url({"mode": "states", "country": category["name"]})
        state_countries_list.append((url, list_item, True))

    state_countries_list.append(gui.next_page_item(response, "state_countries", page))
    state_countries_list = [i for i in state_countries_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, state_countries_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def get_states(addon_handle, country, page):
    page = int(page)
    response = server.get(
        f"/states/{country}/",
        {
            "offset": page * 50,
            "limit": 50,
            "order": "stationcount",
            "reverse": "true",
        },
    ).json()

    states_list = []
    for category in response:
        list_item = xbmcgui.ListItem(category["name"])

        list_item.setInfo(
            "music",
            {
                "title": category["name"],
                "genre": _("{0} stations").format(category["stationcount"]),
            },
        )
        url = utils.build_url(
            # FIXME: sometimes it picks up similarly named states as well,
            # FIXME: like Bavaria, Germany when the user picked Bavaria, Netherlands
            {"mode": "stations_sort", "kind": "bystateexact/" + category["name"]}
        )
        states_list.append((url, list_item, True))

    states_list.append(gui.next_page_item(response, "countries", page, country=country))
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
        list_item = xbmcgui.ListItem(category["name"].title())

        list_item.setInfo(
            "music",
            {
                "title": category["name"].title(),
                "genre": _("{0} stations").format(category["stationcount"]),
            },
        )
        url = utils.build_url(
            {"mode": "stations_sort", "kind": "bylanguageexact/" + category["name"]}
        )
        languages_list.append((url, list_item, True))

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
        list_item = xbmcgui.ListItem(category["name"])

        list_item.setInfo(
            "music",
            {
                "title": category["name"],
                "genre": _("{0} stations").format(category["stationcount"]),
            },
        )
        url = utils.build_url(
            {"mode": "stations_sort", "kind": "bytagexact/" + category["name"]}
        )
        tags_list.append((url, list_item, True))

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
        list_item = xbmcgui.ListItem(category["name"])

        list_item.setInfo(
            "music",
            {
                "title": category["name"],
                "genre": _("{0} stations").format(category["stationcount"]),
            },
        )
        url = utils.build_url(
            {"mode": "stations_sort", "kind": "bycodecexact/" + category["name"]}
        )
        codecs_list.append((url, list_item, True))

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
            response,
            "results",
            page,
            kind=kind,
            search_text=search_text,
            orderby=orderby,
            reverse=reverse,
        )
    )
    results_list = [i for i in results_list if i]

    xbmcplugin.addDirectoryItems(addon_handle, results_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def open_search_by_name(addon_handle):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading(_("Enter station name"))
    keyboard.doModal()
    if keyboard.isConfirmed() and len(keyboard.getText()) > 0:
        open_search_sort_directory(addon_handle, "name", keyboard.getText())


def open_search_by_tags(addon_handle):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading(_("Enter comma-separated tags"))
    keyboard.doModal()
    if keyboard.isConfirmed() and len(keyboard.getText()) > 0:
        open_search_sort_directory(
            addon_handle,
            "tag",
            ",".join([i.strip() for i in keyboard.getText().split(",")]),
        )


def open_custom_url(addon_handle):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading(_("Enter stream URL"))
    keyboard.doModal()
    if keyboard.isConfirmed() and len(keyboard.getText()) > 0:
        gui.station_item(keyboard.getText(), 1)
        xbmcplugin.addDirectoryItems(
            addon_handle, [gui.station_item(keyboard.getText(), 1)]
        )
        xbmcplugin.setContent(addon_handle, "songs")
        xbmcplugin.endOfDirectory(addon_handle)


def get_saved_station_stations(addon_handle):
    stations_list = saved_stations.get_saved_stations()

    xbmcplugin.addDirectoryItems(addon_handle, stations_list)
    xbmcplugin.setContent(addon_handle, "songs")
    xbmcplugin.endOfDirectory(addon_handle)


def vote_for_station(uuid):
    vote_result = server.post("/vote/" + uuid).json()

    if vote_result["ok"]:
        xbmcgui.Dialog().notification(
            "RadioBrowser²", _("Voted for station successfully!")
        )
    else:
        xbmcgui.Dialog().notification(
            "RadioBrowser²",
            _("Voting for station failed: {0}").format(vote_result["message"]),
        )


def play(addon_handle, path, uuid):
    list_item = xbmcgui.ListItem(path=path)
    if len(uuid) > 0:
        click_counter_result = server.post("/url/" + uuid).json()
        xbmcplugin.setResolvedUrl(
            addon_handle, click_counter_result.get("ok", False), list_item
        )  # TODO: add action in case ok is false
    else:
        xbmcplugin.setResolvedUrl(addon_handle, True, list_item)
