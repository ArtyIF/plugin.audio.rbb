import sys
from urllib.parse import parse_qs
import xbmcgui

from resources.lib import routes, server, saved_stations
from resources.lib.locale import localize_string as _


def main():
    args = parse_qs(sys.argv[2][1:])
    mode = args.get("mode", None)

    # initial launch of add-on
    if mode is None:
        routes.root(addon_handle)
    elif mode[0] == "stations":
        server.connect()
        routes.get_stations(
            addon_handle,
            args["kind"][0],
            args.get("page", [0])[0],
            args.get("orderby", ["votes"])[0],
            args.get("reverse", ["true"])[0],
        )
    elif mode[0] == "stations_by":
        routes.open_stations_directory(addon_handle)
    elif mode[0] == "search":
        routes.open_search_directory(addon_handle)
    elif mode[0] == "stations_sort":
        routes.open_stations_sort_directory(addon_handle, args["kind"][0])
    elif mode[0] == "countries":
        server.connect()
        routes.get_countries(addon_handle, args.get("page", [0])[0])
    elif mode[0] == "state_countries":
        server.connect()
        routes.get_state_countries(addon_handle, args.get("page", [0])[0])
    elif mode[0] == "states":
        server.connect()
        routes.get_states(
            addon_handle, args.get("country", [""])[0], args.get("page", [0])[0]
        )
    elif mode[0] == "languages":
        server.connect()
        routes.get_languages(addon_handle, args.get("page", [0])[0])
    elif mode[0] == "tags":
        server.connect()
        routes.get_tags(addon_handle, args.get("page", [0])[0])
    elif mode[0] == "codecs":
        server.connect()
        routes.get_codecs(addon_handle, args.get("page", [0])[0])
    elif mode[0] == "listen":
        server.connect()
        routes.play(addon_handle, args["url"][0], args.get("uuid", [""])[0])
    elif mode[0] == "search_by_name":
        routes.open_search_by_name(addon_handle)
    elif mode[0] == "search_by_tags":
        routes.open_search_by_tags(addon_handle)
    elif mode[0] == "search_sort":
        routes.open_search_sort_directory(
            addon_handle, args["kind"][0], args["search_text"][0]
        )
    elif mode[0] == "saved_stations":
        routes.get_saved_station_stations(addon_handle)
    elif mode[0] == "saved_station_add":
        if args.get("uuid", None):
            saved_stations.add_saved_station(args["uuid"][0], "uuid")
        elif args.get("url", None):
            saved_stations.add_saved_station(args["url"][0], "url")
    elif mode[0] == "saved_station_remove":
        if args.get("uuid", None):
            saved_stations.remove_saved_station(args["uuid"][0], "uuid")
        elif args.get("url", None):
            saved_stations.remove_saved_station(args["url"][0], "url")
    elif mode[0] == "custom_url":
        routes.open_custom_url(addon_handle)
    elif mode[0] == "vote":
        server.connect()
        routes.vote_for_station(args["uuid"][0])
    elif mode[0] == "results":
        server.connect()
        routes.perform_search(
            addon_handle,
            args.get("kind", ["name"])[0],
            args["search_text"][0],
            args.get("orderby", ["votes"])[0],
            args.get("reverse", ["true"])[0],
            args.get("page", [0])[0],
        )
    else:
        notif = xbmcgui.Dialog()
        notif.notification(
            _("RadioBrowser?? internal error! Tell the developer!"),
            _(
                "Add-on tried to access a non-existent mode: {0} (all arguments: {1})"
            ).format(mode[0], args),
            xbmcgui.NOTIFICATION_ERROR,
        )


if __name__ == "__main__":
    addon_handle = int(sys.argv[1])
    main()
