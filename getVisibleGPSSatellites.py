import urllib
import urllib2
import nvector as nv
import numpy as np
import ephem
import datetime
import os
import requests
import simplejson
import math

ELEVATION_BASE_URL = 'https://maps.googleapis.com/maps/api/elevation/json'
numberPointsElevationPath = 5
distanceElevationPath     = 5000
delDistance               = int(distanceElevationPath/numberPointsElevationPath)

url = 'http://celestrak.com/NORAD/elements/gps-ops.txt'
elevationFile = requests.get(url)

# Google Elevation API info
myKey = "AIzaSyAZgMQ6edjbiq3hO5Aq2XhWO5bo0Ot2nfE"

def n_choose_k(n,k):
    return math.factorial(n)/math.factorial(k)/math.factorial(n-k)

# Downloads current NORAD Two-Line Element Sets for GPS
def downloadTLE():
    with open('./files/NORAD_TLE_GPS.txt', 'wb') as f:
        f.write(elevationFile.content)

def getElevationPath(path="", key="", samples="100", **elvtn_args):
      elvtn_args.update({
        'path': path,
        'key': key,
        'samples': samples
      })

      # Create a dictionary for each results[] object
      elevationPathArray = []

      url = ELEVATION_BASE_URL + '?' + urllib.urlencode(elvtn_args)
      response = simplejson.load(urllib.urlopen(url))
      if response["status"] == "OK":
          for resultset in response['results']:
              elevationPathArray.append(resultset['elevation'])
      else:
          elevationPathArray= None

      return elevationPathArray

# Loads a TLE file and creates a list of satellites
def loadTLE(filename):
    f = open(filename)
    satlist = []
    l1 = f.readline()
    while l1:
        l2 = f.readline()
        l3 = f.readline()
        sat = ephem.readtle(l1,l2,l3)
        satlist.append(sat)
        #print sat.name
        l1 = f.readline()

    f.close()
    print "%i satellites loaded"%len(satlist)
    return satlist


def getVisibleGPSSatellites(lat, lon, elev):
    filename = './files/NORAD_TLE_GPS.txt'
    sat      = loadTLE(filename)
    print "Ephemeris data loaded."
    nSat     = len(sat)

    rx           = ephem.Observer()
    rx.elevation = elev
    rx.lat       = np.deg2rad(lat)
    rx.long      = np.deg2rad(lon)
    latlon       = str(lat) + "," + str(lon)

    # Compute satellite locations at time = now and count visible satellites
    sat_alt, sat_az, sat_vis, sat_vis_flag = [], [], [], []
    vs = 0
    too_low = 0
    date_time = datetime.datetime.now()

    rx.date = date_time
    frame   = nv.FrameE(a=6378137, f=1.0/298.257)
    pointA  = frame.GeoPoint(latitude=lat, longitude=lon, z=-elev, degrees=True)
    dist = range(delDistance, (distanceElevationPath+delDistance), delDistance)
    for i in range(0, nSat):
        biif1 = sat[i]
        biif1.compute(rx)
        sat_alt.append(np.rad2deg(biif1.alt))
        sat_az.append( np.rad2deg(biif1.az ))
        if np.rad2deg(biif1.alt) < -30:
            sat_vis_flag.append(0)
            continue
        pointB, _azimuthb = pointA.geo_point(distance=distanceElevationPath, azimuth=np.rad2deg(biif1.az), degrees=True)
        latB, lonB = pointB.latitude_deg, pointB.longitude_deg
        latlonB = str(latB) + "," + str(lonB)
        pathStr = latlon + "|" + latlonB
        elevPath = getElevationPath(pathStr, myKey, (numberPointsElevationPath+1))
        if elevPath is None:
            print "ELEVATIONPATH FAIL"
        else:
            elevPath = elevPath[1:]
            k   = 0
            ang = []
            for el in elevPath:
                ang.append(np.rad2deg(np.arctan2((el - elev), dist[k])))
        #print "dist " + str(k) + " angle is " + str((np.rad2deg(np.arctan2((el - elev), dist[k]))))
                k = k + 1
    #print ("is this value " + str(np.rad2deg(biif1.alt)) + " greater than " + str(np.max(az)))

        if np.rad2deg(biif1.alt) > np.max(ang):
            vs = vs + 1
            sat_vis.append(biif1)
            sat_vis_flag.append(1)
            if (np.rad2deg(biif1.alt) - np.max(ang)) < 15:
                too_low = too_low + 1.0
        else:
            sat_vis_flag.append(0)

    by_satellite = ([{"sat_alt": altitude, "sat_az": azimuth, "sat_vis_flag": visibility}
                            for altitude, azimuth, visibility in zip(sat_alt, sat_az, sat_vis_flag)])

    #print(by_satellite)

    number_visible = sat_vis_flag.count(1)

    print (str(number_visible) + " are visible")
#    print by_satellite

    too_close = 0

    for i in range(0, number_visible):
        for j in range(i+1, number_visible):
            ang = float(repr(ephem.separation(sat_vis[i], sat_vis[j])))*180/ephem.pi
            if ephem.degrees(ang) < 30:
                too_close = too_close + 1.0

    s = n_choose_k(number_visible, 2)
    print str(s) + " is the nchoosek value"
    too_close_metric = float(s-too_close)/s
    too_low_metric   = 1.0 - float(too_low/number_visible)
    constellation_quality = (too_close_metric + too_low_metric)/2.0

    print too_close_metric, too_low_metric

    return number_visible, by_satellite, constellation_quality
