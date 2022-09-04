import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()

#     0-29999: Built-in strings from Kodi
# 30000-32999: Add-on strings
# 33000-39999: Built-in strings from Kodi
# Built-in strings from:
# https://github.com/xbmc/xbmc/blob/master/addons/resource.language.en_gb/resources/strings.po
LOCALIZED_STRINGS = {
    16017: "Enter search string",
    19140: "Search...",
    30000: "RadioBrowser² internal error! Tell the developer!",
    30001: "Add-on tried to access a non-existent mode: {0} (all arguments: {1})",
    30002: "Page {0}",
    30003: "[B]{0} votes[/B]",
    30004: "[B]Offline![/B]",
    30005: "Add to Saved Stations",
    30006: "Remove from Saved Stations",
    30007: "Vote for Station",
    30008: "Most Voted First",
    30009: "Least Voted First",
    30010: "Most Listeners First",
    30011: "Least Listeners First",
    30012: "A-Z",
    30013: "Z-A",
    30014: "Highest Bitrate First",
    30015: "Lowest/Undefined Bitrate First",
    30016: "Oldest Change First",
    30017: "Newest Change First",
    30018: "Random",
    30019: "Saved Stations",
    30020: "Most Voted Stations",
    30021: "Trending Stations",
    30022: "Stations Recently Played by Others",
    30023: "Recently Added/Changed Stations",
    30024: "Stations by...",
    30025: "Custom URL",
    30026: "Stations by Country",
    30027: "Stations by State",
    30028: "Stations by Language",
    30029: "Stations by Tag",
    30030: "Stations by Codec",
    30031: "All Stations",
    30032: "Search by Name",
    30033: "Search by Tags",
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
