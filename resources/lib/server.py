import socket
import random
import requests

headers = {"User-Agent": "RadioBrowser2/0.4.0"}
server_url = ""


def get(path, params={}, **kwargs):
    return requests.get(server_url + path, headers=headers, params=params, **kwargs)


def post(path, params={}, **kwargs):
    return requests.post(server_url + path, headers=headers, params=params, **kwargs)


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
    # FIXME: if you remove the return below it will repeatedly try to connect to that server, after which it'll raise an exception
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
                    f"requests.get({uri}) returned status code {data.status_code}"
                )
        except ConnectionError:
            continue
    raise ConnectionError("Could not connect to any of radio-browser.info servers")


def connect():
    global server_url
    server_url = f"https://{get_appropriate_server()}/json"
