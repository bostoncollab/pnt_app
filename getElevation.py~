import simplejson
import urllib
import pprint

ELEVATION_BASE_URL = 'https://maps.googleapis.com/maps/api/elevation/json'

def getElevation(locations, key="", **elvtn_args):
    elvtn_args.update({
        'locations': locations,
        'key': key
    })
    url = ELEVATION_BASE_URL + '?' + urllib.urlencode(elvtn_args)
    response = simplejson.load(urllib.urlopen(url))
    elevation_reading = response["results"][0]["elevation"]
    pprint.pprint(response)
    # return a single elevation reading
    return elevation_reading

# getElevation("42.356872,-71.057494") # for testing
    # Create a dictionary for each results[] object
    # elevationArray = []

    # for resultset in response['results']:
    #     elevationArray.append(resultset['elevation'])
    # return elevationArray
