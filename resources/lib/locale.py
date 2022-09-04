import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()

#     0-29999: Built-in strings from Kodi
# 30000-32999: Add-on strings
# 33000-39999: Built-in strings from Kodi
# Built-in strings from:
# https://github.com/xbmc/xbmc/blob/master/addons/resource.language.en_gb/resources/strings.po
LOCALIZED_STRINGS = {
    19140: "Search...",
    30000: "RadioBrowser² internal error! Tell the developer!",
    30001: "Add-on tried to access a non-existent mode: {0} (all arguments: {1})",
    30002: "Page {0}",
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
