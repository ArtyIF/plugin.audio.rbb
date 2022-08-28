import sys
import xbmcgui
from urllib.parse import parse_qs

from resources.lib import routes, server


def main():
    args = parse_qs(sys.argv[2][1:])
    mode = args.get("mode", None)

    # initial launch of add-on
    if mode is None:
        routes.root(addon_handle)
    elif mode[0] == "stations":
        routes.get_stations(
            addon_handle,
            args["kind"][0],
            args.get("page", [0])[0],
            args.get("orderby", ["name"])[0],
        )
    elif mode[0] == "countries":
        routes.get_countries(addon_handle, args.get("page", [0])[0])
    elif mode[0] == "statecountries":
        routes.get_state_countries(addon_handle, args.get("page", [0])[0])
    elif mode[0] == "states":
        routes.get_states(
            addon_handle, args.get("state", [""])[0], args.get("page", [0])[0]
        )
    elif mode[0] == "languages":
        routes.get_languages(
            addon_handle, args.get("page", [0])[0]
        )
    elif mode[0] == "listen":
        routes.play(addon_handle, args["url"][0], args["uuid"][0])
    else:
        notif = xbmcgui.Dialog()
        notif.notification(
            "RadioBrowser² internal error! Tell the developer!",
            f"Add-on tried to access a non-existent mode: {mode[0]} (all arguments: {args})",
            xbmcgui.NOTIFICATION_ERROR,
        )


if __name__ == "__main__":
    server.connect()
    addon_handle = int(sys.argv[1])
    main()
