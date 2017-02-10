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

ELEVATION_BASE_URL        = 'https://maps.googleapis.com/maps/api/elevation/json'
numberPointsElevationPath = 500
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
    print "%i satellites loaded" % len(satlist)
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
    satAlt, satAz, satVis, satVisFlag = [], [], [], []
    vs = 0
    tooLow = 0
    dateTime = datetime.datetime.now()

    rx.date = dateTime
    frame   = nv.FrameE(a=6378137, f=1.0/298.257)
    pointA  = frame.GeoPoint(latitude=lat, longitude=lon, z=-elev, degrees=True)
    dist = range(delDistance, (distanceElevationPath+delDistance), delDistance)
    for i in range(0, nSat):
        biif1 = sat[i]
        biif1.compute(rx)
        satAlt.append(np.rad2deg(biif1.alt))
        satAz.append( np.rad2deg(biif1.az ))
        if np.rad2deg(biif1.alt) < -30:
            satVisFlag.append(0)
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
            satVis.append(biif1)
            satVisFlag.append(1)
            if (np.rad2deg(biif1.alt) - np.max(ang)) < 15:
                tooLow = tooLow + 1.0
        else:
            satVisFlag.append(0)

    bySatellite = ([{"satAlt": altitude, "satAz": azimuth, "satVisFlag": visibility}
                            for altitude, azimuth, visibility in zip(satAlt, satAz, satVisFlag)])

    #print(by_satellite)

    numberVisible = satVisFlag.count(1)

    print (str(numberVisible) + " are visible")
#    print by_satellite

    tooClose = 0

    for i in range(0, numberVisible):
        for j in range(i+1, numberVisible):
            ang = float(repr(ephem.separation(satVis[i], satVis[j])))*180/ephem.pi
            if ephem.degrees(ang) < 30:
                tooClose = tooClose + 1.0

    s = n_choose_k(numberVisible, 2)
    print str(s) + " is the nchoosek value"
    tooCloseMetric  = float(s-tooClose)/s
    tooLowMetric = 1.0 - float(tooLow/numberVisible)
    constellationQuality = (tooCloseMetric + tooLowMetric)/2.0

    print tooCloseMetric, tooLowMetric

    return numberVisible, bySatellite, constellationQuality
