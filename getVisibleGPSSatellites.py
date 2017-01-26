import numpy as np
import ephem
import datetime
import os
import pycurl
import json
import jsonify

ELEVATION_BASE_URL = 'https://maps.googleapis.com/maps/api/elevation/json'


# Google Elevation API info
myKey = "AIzaSyAZgMQ6edjbiq3hO5Aq2XhWO5bo0Ot2nfE"

# Downloads current NORAD Two-Line Element Sets for GPS
def downloadTLE():
    with open('./files/NORAD_TLE_GPS.txt', 'wb') as f:
        c = pycurl.Curl()
        c.setopt(c.URL, 'http://celestrak.com/NORAD/elements/gps-ops.txt')
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()

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


def getVisibleGPSSatellites(lat, lon):
    filename = './files/NORAD_TLE_GPS.txt'
    sat      = loadTLE(filename)
    nSat     = len(sat)

    rx      = ephem.Observer()
    rx.lat  = np.deg2rad(lat)
    rx.long = np.deg2rad(lon)

    # Compute satellite locations at time = now and count visible satellites
    sat_alt, sat_az, sat_vis, sat_vis_flag = [], [], [], []
    vs = 0
    too_low = 0
    date_time = datetime.datetime.now()

    rx.date = date_time
    for i in range(0, nSat):
        biif1 = sat[i]
        biif1.compute(rx)
        sat_alt.append(np.rad2deg(biif1.alt))
        sat_az.append( np.rad2deg(biif1.az ))
        if np.rad2deg(biif1.alt) > 10:
            vs = vs + 1
            sat_vis.append(biif1)
            sat_vis_flag.append(1)
            if np.rad2deg(biif1.alt) < 20:
                too_low = too_low + 1.0
        else:
            sat_vis_flag.append(0)
    
    by_satellite = ([{"sat_alt": altitude, "sat_az": azimuth, "sat_vis_flag": visibility}
                            for altitude, azimuth, visibility in zip(sat_alt, sat_az, sat_vis_flag)])

    number_visible = sat_vis_flag.count(1)

    print (str(number_visible) + " are visible")
#    print by_satellite
    
    too_close = 0
    s = 0
    for i in range(0, number_visible):
        for j in range(i+1, number_visible):
            s = s + 1.0
            ang = float(repr(ephem.separation(sat_vis[i], sat_vis[j])))*180/ephem.pi
#            print ang
            if ephem.degrees(ang) < 35:
                too_close = too_close + 1.0

    too_close_metric = float(s-too_close)/s 
    too_low_metric   = 1.0 - float(too_low/number_visible) 
    constellation_quality = (too_close_metric + too_low_metric)/2.0           
    print too_close_metric, too_low_metric
    # print ({'sat_alt': sat_alt, 'sat_az': sat_az, 'sat_vis': sat_vis})
    # return {'sat_alt': sat_alt, 'sat_az': sat_az, 'sat_vis': sat_vis}

    return number_visible, by_satellite, constellation_quality


