import json
from geopy import distance


def makeCoordinates(coords):
    result = []
    i = 0
    while i < len(coords):
        if len(coords[i]) % 2 != 0:
            raise Exception('Invalid coordinates {}', coords)

        lat = coords[i][0]
        lng = coords[i][1]
        result.append((lat, lng))
        i += 2

    return result


def flatten(stack):
    result = []
    while(len(stack) > 0):
        if isinstance(stack[0][0], float) or isinstance(stack[0][0], int):
            result += makeCoordinates(stack)
            stack.pop(0)
            continue

        item = stack[0]
        if isinstance(item[0][0], float) or isinstance(item[0][0], int):
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
    lat = float(coordinates[0][1])
    lng = float(coordinates[0][0])

    minLat = 180
    minLng = 90
    maxLat = -180
    maxLng = -90

    for coord in coordinates:
        lat = float(coord[1])
        lng = float(coord[0])

        if lat > 90:
            lat = 90
        if lat < -90:
            lat = -90
        if lng > 180:
            lng = 180
        if lng < -180:
            lng = -180

        minLat = min(minLat, lat)
        minLng = min(minLng, lng)
        maxLat = max(maxLat, lat)
        maxLng = max(maxLng, lng)

    return {
        'southWest': {
            'lat': minLat,
            'lng': minLng
        },
        'northEast': {
            'lat': maxLat,
            'lng': maxLng
        }
    }


with open('./countries.geojson') as f:
    data = json.load(f)

countries = []
for feature in data['features']:
    props = feature['properties']

    boxes = bounds(flatten(feature['geometry']['coordinates']))

    countries.append({
        'name': props['ADMIN'],
        'iso': props['ISO_A3'],
        'bounds': boxes
    })


with open('countries_bounds.json', 'w') as out:
    json.dump(countries, out, indent=2)
