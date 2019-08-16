import json


def makeCoordinates(coords):
    if len(coords) % 2 != 0:
        raise Exception('Invalid coordinates {}', coords)

    i = 0
    result = []

    while i < len(coords):
        lat = coords[i]
        lng = coords[i+1]
        i += 2
        result.append((lat, lng))

    return result


def flatten(stack):
    result = []
    while(len(stack) > 0):
        item = stack[0]
        if isinstance(item[0], float) or isinstance(item[0], int):
            result += makeCoordinates(item)
            stack.pop(0)
        else:
            flat = []
            for i in item:
                flat += i
            stack[0] = flat
    return result


def bounds(coordinates):
    # find min/max
    minLat = 180
    minLng = 90
    maxLat = -180
    maxLng = -90

    for coord in coordinates:
        lat = float(coord[0])
        lng = float(coord[1])
        minLat = min(minLat, lat)
        minLng = min(minLng, lng)
        maxLat = max(maxLat, lat)
        maxLng = max(maxLng, lng)

    return {
        'southWest': {
            'lat': round(minLat, 6),
            'lng': round(minLng, 6)
        },
        'northEast': {
            'lat': round(maxLat, 6),
            'lng': round(maxLng, 6)
        }
    }


with open('./countries.geojson') as f:
    data = json.load(f)


countries = []
for feature in data['features']:
    props = feature['properties']
    countries.append({
        'name': props['ADMIN'],
        'iso': props['ISO_A3'],
        'bounds': bounds(flatten(feature['geometry']['coordinates']))
    })


with open('countries_bounds.json', 'w') as out:
    json.dump(countries, out, indent=2)
