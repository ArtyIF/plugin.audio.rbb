import sys
from urllib.parse import urlencode


def build_url(query):
    base_url = sys.argv[0]
    return base_url + "?" + urlencode(query)