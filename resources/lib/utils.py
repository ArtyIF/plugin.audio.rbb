import sys
from urllib.parse import urlencode
import xbmcgui


def build_url(query):
    base_url = sys.argv[0]
    return base_url + "?" + urlencode(query)


def next_page_item(response, mode, current_page, params={}):
    if len(response) == 50:
        # TODO: override the titlebar to indicate the page and kind if possible
        li = xbmcgui.ListItem(f"Next Page")
        li.setInfo("music", {"title": "Next Page", "genre": f"Page {current_page+2}"})
        query = {"mode": mode, "page": current_page + 1}
        query.update(params)
        url = build_url(query)
        return (url, li, True)
