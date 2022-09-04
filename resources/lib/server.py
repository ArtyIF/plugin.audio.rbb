import socket
import random
import requests

from resources.lib.locale import localize_string as _

headers = {"User-Agent": "RadioBrowser2/0.10.0"}
server_url = ""


def get(path, params={}, **kwargs):
    if server_url == "":
        raise ConnectionError(_("Not connected to server"))
    return requests.get(
        server_url + path, headers=headers, params=params, timeout=5.0, **kwargs
    )


def post(path, params={}, **kwargs):
    if server_url == "":
        raise ConnectionError(_("Not connected to server"))
    return requests.post(
        server_url + path, headers=headers, params=params, timeout=5.0, **kwargs
    )


# from https://api.radio-browser.info/examples/serverlist_python3.py
def get_radiobrowser_base_urls():
    hosts = []
    ips = socket.getaddrinfo("all.api.radio-browser.info", 80, 0, 0, socket.IPPROTO_TCP)
    for ip_tuple in ips:
        ip_address = ip_tuple[4][0]

        host_addr = socket.gethostbyaddr(ip_address)
        if host_addr[0] not in hosts:
            hosts.append(host_addr[0])

    hosts.sort()
    return hosts


def get_appropriate_server():
    # FIXME: if you remove the return below it will repeatedly try to connect to
    # FIXME: that server, after which it'll raise an exception
    # TODO: enable connecting to other servers
    return "de1.api.radio-browser.info"
    servers = get_radiobrowser_base_urls()
    for server_base in servers:
        uri = f"https://{server_base}/json/stats"

        try:
            data = get(uri)
            if data.status_code == 200:
                return server_base
            else:
                raise ConnectionError(
                    _("requests.get({0}) returned status code {1}").format(
                        uri, data.status_code
                    )
                )
        except ConnectionError:
            continue
    raise ConnectionError(_("Could not connect to any of radio-browser.info servers"))


def connect():
    global server_url
    server_url = f"https://{get_appropriate_server()}/json"
