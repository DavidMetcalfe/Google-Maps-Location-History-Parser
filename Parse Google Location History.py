import json
import os
import sys

# Allow passing the Location History file or folder as an argument. Default
# to the legacy single-file layout described in the original README.
path = sys.argv[1] if len(sys.argv) > 1 else 'Location History.json'

# Google Takeout's Location History comes in two shapes:
#   * Legacy: a single file (e.g. "Location History.json") with a top-level
#     "locations" array of {"latitudeE7", "longitudeE7"} dicts.
#   * Current: a folder (e.g. "Semantic Location History/2020/") of per-month
#     JSON files with a top-level "timelineObjects" array of "placeVisit"
#     and "activitySegment" dicts. Settings.json holds reporting metadata,
#     not history entries, so it is skipped.
if os.path.isdir(path):
    json_files = []
    for root, _dirs, files in os.walk(path):
        for name in files:
            if name.lower().endswith('.json') and name != 'Settings.json':
                json_files.append(os.path.join(root, name))
    json_files.sort()
else:
    json_files = [path]

entries = []
for fp in json_files:
    with open(fp) as f:
        # Load in Google Location History data.
        data = json.load(f)
    # Prefer the new schema; fall back to legacy for older exports.
    entries.extend(data.get('timelineObjects') or data.get('locations') or [])

d = []

counter = 0

for i in entries:
    # New-schema placeVisit: {"placeVisit": {"location": {"latitudeE7": ...}}}
    if 'placeVisit' in i:
        loc = i['placeVisit'].get('location', {})
        if 'latitudeE7' in loc and 'longitudeE7' in loc:
            d.append((loc['latitudeE7'], loc['longitudeE7']))
    # New-schema activitySegment: {"activitySegment": {"startLocation": ...,
    # "endLocation": ...}}. Emit both endpoints so the path between them is
    # represented in the output.
    elif 'activitySegment' in i:
        seg = i['activitySegment']
        for key in ('startLocation', 'endLocation'):
            loc = seg.get(key, {})
            if 'latitudeE7' in loc and 'longitudeE7' in loc:
                d.append((loc['latitudeE7'], loc['longitudeE7']))
    # Legacy entry: {"latitudeE7": ..., "longitudeE7": ...} at the top level.
    elif 'latitudeE7' in i and 'longitudeE7' in i:
        d.append((i['latitudeE7'], i['longitudeE7']))

    counter += 1
    if not counter % 10000:
        # Print update every 10k entries (useful for large data).
        print("Counter: {}".format(counter))

def convertCoords(coord):
    # Convert E7 lat/long format to decimal.
    return coord / 1e7

def uniquify(seq):
    # Remove duplicate lat/long data.
    # Not order preserving.
    return list(set(seq))

final = uniquify(d)

print("------------")
print("Unique lat/long entries remaining: {}".format(len(final)))
print("------------")
print("Writing output to file.")
with open("output.txt", 'w') as o:
    o.write("{}".format(final))
