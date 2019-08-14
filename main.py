import json


def flatten(arr, result=[]):
    if not isinstance(arr[0], list):
        return [(arr[0], arr[1])]

    for item in arr:
        result += flatten(item, result)

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
    json.dump(countries, out, indent=2)
