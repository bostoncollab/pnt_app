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
    if response["status"] == "OK":
        elevation_reading = response["results"][0]["elevation"]
        pprint.pprint(response)
    else:
        elevation_reading = None
    # return a single elevation reading
    return elevation_reading
