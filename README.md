# Google Maps Location History Parser

The included script will parse the extracted JSON data from Google Maps' Location History, and output a list of unique lat/long coordinates in a `.txt` file for your own use.

Older tutorials concerning Google Latitude, and Google Maps' Timeline would require raw extraction, or looping through exporting KML files, etc. Nowadays, [Google Takeout](https://takeout.google.com/settings/takeout) supports exporting one's Location History easily.

## Steps to export data
1. Visit [Google Takeout](https://takeout.google.com/settings/takeout).
2. Click **Select None** at the top of the list to deselect all other options.
3. Navigate down to **Location History** and select it. Leave the default export at JSON.
4. Click **Next**, and choose your File Type, Archive Size, and Delivery Method.
5. Once the file is downloaded and unarchived, proceed to the next steps.

## Parse your export data

1. Download `Parse Google Location History.py` and place the script in the same directory as your export.
2. Run the script from your chosen command line, passing the path to your Location History file or folder:
   * **Legacy export** (pre-2020, single file): `python "Parse Google Location History.py" "Location History.json"`
   * **Current Takeout export** (2020+, folder of monthly JSONs): `python "Parse Google Location History.py" "Semantic Location History"`
   * You can also point it at a specific year folder, e.g. `Semantic Location History/2020`, or omit the argument to default to a `Location History.json` in the current directory.
3. A deduplicated list of unique `latitudeE7` / `longitudeE7` coordinates will be written to `output.txt`.

## Notes

There's an additional function included for converting the Lat/Long coordinates in E7 format to decimal. It's not made use of in the script, but it may be helpful to any interested.
