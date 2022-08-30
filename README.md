# RadioBrowser²
*A browser for RadioBrowser*

**RadioBrowser²** (Radio Browser Browser, or Radio Browser Squared) is a music add-on to browse the radio station list on [radio-browser.info](https://www.radio-browser.info/).

## Progress
This plugin is still in an early stage. Here's what it can do and what's planned:
- [x] List most voted stations
- [x] List most clicked (trending) stations
- [x] List recently clicked (recently played by others) stations
- [x] List recently added/changed stations
- [x] List all stations alphabetically
- [x] Split lists in pages (50 stations each)
- [x] Display station icon
- [x] Display station tags, location and language (all in Genre section for now)
- [x] Play the stations
- [x] List stations by:
- - [x] Country
- - [x] State
- - [x] Language
- - [x] Tag
- - [x] Codec
- [x] Let the user choose to sort stations
- [x] Filter states by country
- [x] Search stations by name and tags
- [x] Add/remove stations to/from Saved Stations
- [x] Vote for stations
- [ ] Localization:
- - [ ] Of the main interface
- - [ ] Of locations and countries
- - [ ] Of tags, if possible

## Install Guide
1. Clone the repository
2. Put all the files in an **UNCOMPRESSED** zip file (can be done on Windows compression ratio can be configured in [7-Zip](https://www.7-zip.org/). For Linux and macOS users, there's a file called `build.sh` that creates the zip file and places it in the `build` directory)
3. In Kodi, go to "Settings" -> "System" -> "Add-ons", enable "Unknown Sources" and agree to the warning
4. Go back to the "Settings" menu, then to "Add-ons" -> "Install from zip file" and choose the created zip file
5. After installation, the add-on will be in "Music add-ons"

From v0.5.0 onwards, I include the pre-zipped add-on in the releases. I also plan to get this on the Kodi official repo someday.
