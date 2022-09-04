import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()

#     0-29999: Built-in strings from Kodi
# 30000-32999: Add-on strings
# 33000-39999: Built-in strings from Kodi
# Built-in strings from:
# https://github.com/xbmc/xbmc/blob/master/addons/resource.language.en_gb/resources/strings.po
LOCALIZED_STRINGS = {
    19140: "Search...", # TODO: check if this the string that's needed
    30000: "RadioBrowser² internal error! Tell the developer!",
    30001: "Add-on tried to access a non-existent mode: %s (all arguments: %s)",
    30002: "Page %i",
    33078: "Next page",
}


def localize_context(str_id):
    if 30000 <= str_id < 33000:
        return ADDON.getLocalizedString(str_id)
    return xbmc.getLocalizedString(str_id)


def localize_string(unlocalized_string):
    try:
        return localize_context(
            list(LOCALIZED_STRINGS.keys())[
                list(LOCALIZED_STRINGS.values()).index(unlocalized_string)
            ]
        )
    except ValueError:
        return f"MISSING IN LOCALIZED_STRINGS: {unlocalized_string}"
