"""A module that stores common server functions."""
# TODO: refactor into a class
import random
import socket
from typing import Optional
import urllib
import urllib.request

import requests
import xbmcgui

from resources.lib.locale import localize_string as _

HEADERS = {"User-Agent": "RadioBrowser2/1.0.0"}
SERVER_URL = ""


def get(
    path: str, params: Optional[dict[str, str]] = None, **kwargs: dict
) -> requests.Response:
    """
    Sends a GET request to a selected RadioBrowser server.

    Args:
        path (str): API path.
        params (dict[str, str] | None, optional): Parameters passed to the server. Defaults to None.

    Raises:
        ConnectionError: Raised when there is no connection to a server.

    Returns:
        requests.Response: A resulting response.
    """
    if SERVER_URL == "":
        raise ConnectionError(_("Not connected to server"))
    return requests.get(
        SERVER_URL + path, headers=HEADERS, params=params, timeout=5.0, **kwargs
    )


def post(
    path: str, params: Optional[dict[str, str]] = None, **kwargs: dict
) -> requests.Response:
    """
    Sends a POST request to a selected RadioBrowser server.

    Args:
        path (str): API path.
        params (dict[str, str] | None, optional): Parameters passed to the server. Defaults to None.

    Raises:
        ConnectionError: Raised when there is no connection to a server.

    Returns:
        requests.Response: A resulting response.
    """
    if SERVER_URL == "":
        raise ConnectionError(_("Not connected to server"))
    return requests.post(
        SERVER_URL + path, headers=HEADERS, params=params, timeout=5.0, **kwargs
    )


# from https://api.radio-browser.info/examples/serverlist_python3.py
def get_radiobrowser_base_urls() -> list:
    """
    Gets available RadioBrowser server URLs from the DNS record.

    Returns:
        list: A list containing all available servers.
    """
    hosts = []
    ips = socket.getaddrinfo("all.api.radio-browser.info", 80, 0, 0, socket.IPPROTO_TCP)
    for ip_tuple in ips:
        ip_address = ip_tuple[4][0]

        host_addr = socket.gethostbyaddr(ip_address)
        if host_addr[0] not in hosts:
            hosts.append(host_addr[0])

    hosts.sort()
    return hosts


def get_appropriate_server() -> str:
    """
    Tries to get a random working RadioBrowser server.

    Raises:
        ConnectionError: Raised when no RadioBrowser servers are available.

    Returns:
        str: The appropriate server.
    """
    servers = get_radiobrowser_base_urls()
    random.shuffle(servers)

    for server_base in servers:
        uri = f"https://{server_base}/json/stats"

        try:
            req = urllib.request.Request(uri)
            req.add_header("User-Agent", HEADERS["User-Agent"])
            req.add_header("Content-Type", "application/json")

            response = urllib.request.urlopen(req)
            data = response.read()
            response.close()

            if response.getcode() == 200:
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
    """Connects to a random RadioBrowser server."""
    global SERVER_URL
    try:
        SERVER_URL = f"https://{get_appropriate_server()}/json"
    except ConnectionError:
        xbmcgui.Dialog().notification("Connection error", "Put a message here later") # TODO: LOCALIZE THIS
