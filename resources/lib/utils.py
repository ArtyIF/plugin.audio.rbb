"""A module that stores miscellaneous common functions."""

import sys
from urllib.parse import urlencode


def build_url(query: dict[str, str]) -> str:
    """Builds a plugin URL from the query.

    Args:
        query (dict[str, str]): A dictionary containing all parameters to be passed.

    Returns:
        str: A plugin URL.
    """
    base_url = sys.argv[0]
    return base_url + "?" + urlencode(query)
