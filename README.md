# RadioBrowser²
*A browser for RadioBrowser*

**RadioBrowser²** (Radio Browser Browser, or Radio Browser Squared) is a music add-on to browse the radio station list on [radio-browser.info](https://www.radio-browser.info/).

## Progress
This plugin is still in a very early stage. Here's what it can do and what's planned:
- [x] List most voted stations
- [x] List most clicked (trending) stations
- [x] List recently clicked (recently played by others) stations
- [x] List recently added/changed stations
- [x] List all stations alphabetically
- [x] Split lists in pages (50 stations each)
- [x] Display station icon
- [x] Display station tags, location and language (all in Genre section for now)
- [x] Play the stations
- [ ] Add/remove stations to/from Favourites
- [ ] List stations by:
- - [ ] Country
- - [ ] State
- - [ ] Language
- - [ ] Tag
- - [ ] Codec
- [ ] Search stations by different things
- [ ] Localization:
- - [ ] Of the main interface
- - [ ] Of locations and countries
- - [ ] Of tags, if possible

## Install Guide
1. Clone the repository
2. Remove README.md (just in case)
3. Put all the other files in an __UNCOMPRESSED__ zip file (can be done on Linux and macOS with `zip -0 -r plugin.zip *`, and on Windows compression ratio can be configured in [7-Zip](https://www.7-zip.org/))
4. In Kodi, go to "Settings" -> "System" -> "Add-ons", enable "Unknown Sources" and agree to the warning
5. Go back to the "Settings" menu, then to "Add-ons" -> "Install from zip file" and choose the created zip file
6. After installation, the add-on will be in "Music add-ons"

After the extension is ready enough, I will generate the zip files myself, as well as upload it to Kodi repositories.