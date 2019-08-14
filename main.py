import json


def flatten(arr):
    stack = arr
    result = []
    while(len(stack) > 0):
        item = stack[0]
        if not isinstance(item[0], list):
            result += [(item[0], item[1])]
            stack.pop()
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
        lat = coord[0]
        lng = coord[1]
        minLat = min(minLat, lng)
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
    json.dump(countries, out)#, indent=2)
