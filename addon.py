import sys
from urllib.parse import urlencode, parse_qs

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
    elif mode[0] == "categories":
        routes.get_categories(
            addon_handle,
            args["ls"][0],
            args["kind"][0],
            args.get("page", [0])[0],
        )
    elif mode[0] == "listen":
        routes.play(addon_handle, args["url"][0], args["uuid"][0])


if __name__ == "__main__":
    server.connect()
    addon_handle = int(sys.argv[1])
    main()
