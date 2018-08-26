import json

with open('Location History.json') as f:
    # Load in Google Location History data.
    data = json.load(f)

d = []

counter = 0

for i in data['locations']:
    # Loop through JSON, append useful data to list.
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
