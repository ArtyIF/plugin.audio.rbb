import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()

#     0-29999: Built-in strings from Kodi
# 30000-32999: Add-on strings
# 33000-39999: Built-in strings from Kodi
# Built-in strings from:
# https://github.com/xbmc/xbmc/blob/master/addons/resource.language.en_gb/resources/strings.po
LOCALIZED_STRINGS = {
    590: "Random",
    16017: "Enter search string",
    19140: "Search...",
    30000: "RadioBrowser² internal error! Tell the developer!",
    30001: "Add-on tried to access a non-existent mode: {0} (all arguments: {1})",
    30002: "Page {0}",
    30003: "[B]{0} votes[/B]",
    30004: "[B]Offline![/B]",
    30005: "Add to saved stations",
    30006: "Remove from saved stations",
    30007: "Vote for station",
    30008: "Most voted first",
    30009: "Least voted first",
    30010: "Most listeners first",
    30011: "Least listeners first",
    30012: "A-Z",
    30013: "Z-A",
    30014: "Highest bitrate first",
    30015: "Lowest/undefined bitrate first",
    30016: "Oldest change first",
    30017: "Newest change first",
    30018: "JSON decode error occured while loading saved stations, resetting stations...",
    30019: "Saved stations",
    30020: "Most voted stations",
    30021: "Trending stations",
    30022: "Stations recently played by others",
    30023: "Recently added/changed stations",
    30024: "Stations by...",
    30025: "Custom URL",
    30026: "Stations by country",
    30027: "Stations by state",
    30028: "Stations by language",
    30029: "Stations by tag",
    30030: "Stations by codec",
    30031: "All stations",
    30032: "Search by name",
    30033: "Search by tags",
    30034: "{0} stations",
    30035: "{0} total stations",
    30036: "Enter comma-separated tags",
    30037: "Enter stream URL",
    30038: "Voted for station",
    30039: "Voted successfully",
    30040: "Voting error",
    30041: "Voting failed: {0}",
    30042: "Station saved",
    30043: "Saved successfully",
    30044: "Station removed",
    30045: "Remove successfully",
    30046: "Not connected to server",
    30047: "requests.get({0}) returned status code {1}",
    30048: "Could not connect to any of radio-browser.info servers",
    33078: "Next page",
}


def localize_context(str_id):
    result = ""
    if 30000 <= str_id < 33000:
        result = ADDON.getLocalizedString(str_id)
    else:
        result = xbmc.getLocalizedString(str_id)
    if len(result) == 0:
        raise KeyError(str_id)
    return result


def localize_string(unlocalized_string):
    try:
        return localize_context(
            list(LOCALIZED_STRINGS.keys())[
                list(LOCALIZED_STRINGS.values()).index(unlocalized_string)
            ]
        )
    except ValueError:
        return f"[B][COLOR red]MISSING IN LOCALIZED_STRINGS:[/COLOR][/B] {unlocalized_string}"
    except KeyError:
        return f"[B][COLOR red]MISSING IN PO FILE:[/COLOR][/B] {unlocalized_string}"
