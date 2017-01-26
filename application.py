import random

from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api
from werkzeug.exceptions import BadRequest

from getElevation import getElevation
from getVisibleGPSSatellites import downloadTLE, getVisibleGPSSatellites

app = Flask(__name__)
CORS(app)
api = Api(app)

class Ping(Resource):
    def get(self):
        return {'pong': True}

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

    	# pass in a lat & long to the elevation query and get result

        if random.random() > .9:
            downloadTLE()
        visible_satellites, satellite_details, constellation_quality = getVisibleGPSSatellites(latitudevalue, latitudevalue)
    	total_response = {'latitude':   latitude_string,
   		      'longitude':  longitude_string,
  		      'elevation':  elevation_query_response,
                      'satellite_details': satellite_details,
                      'no_visible_satellites': visible_satellites,
                      'constellation_quality': constellation_quality}
    	return total_response

api.add_resource(LocationAPI, '/data')
api.add_resource(Ping, '/ping')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
