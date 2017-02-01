from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
from werkzeug.exceptions import BadRequest

from getElevation import getElevation
from getVisibleGPSSatellites import downloadTLE, getVisibleGPSSatellites

# EB looks for an 'application' callable by default.
application = Flask(__name__)
CORS(application)
api = Api(application)

#initialize counter to download filename
counter = 0

class LeafletMap(Resource):
    def get(self):
        return application.send_static_file('index.html')

class About(Resource):
    def get(self):
        return 'This is a PNT RESTful web service!'

class Ping(Resource):
    def get(self):
        return {'ping': True}

class LocationAPI(Resource):
    def get(self):
    	latitude_string  = request.args.get('latitude')
    	longitude_string = request.args.get('longitude')
        if not latitude_string or not longitude_string:
            raise BadRequest('Must pass latitude and longitude')
        latitudevalue = float(latitude_string)
        longitudevalue = float(longitude_string)
    	querylocation =  '%s,%s' %(latitude_string, longitude_string)

    	# pass in a lat & long to the elevation query and get result
    	elevation_query_response = getElevation(querylocation) # get the elevation according to the queried location

    	# pass in a lat & long to the visible satellites query and get result
        visible_satellites, satellite_details, constellation_quality = getVisibleGPSSatellites(latitudevalue, longitudevalue, elevation_query_response)

        global counter
        if counter % 1000 == 0:
            downloadTLE()

        # compile JSON
        total_response = {'latitude':   latitude_string,
   		                  'longitude':  longitude_string,
  		                  'elevation':  elevation_query_response,
                          'satellite_details': satellite_details,
                          'no_visible_satellites': visible_satellites,
                          'constellation_quality': constellation_quality}
    	return total_response

        # download the file if there have been atleast X calls without a download
        counter += 1
        # print "counter is %d" % counter

api.add_resource(LeafletMap,'/')
api.add_resource(LocationAPI, '/data')
api.add_resource(Ping, '/ping')
api.add_resource(About, '/about')

if __name__ == '__main__':
    application.run()
