from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
from werkzeug.exceptions import BadRequest

from getElevation import getElevation
from getVisibleGPSSatellites import downloadTLE, getVisibleGPSSatellites
from getEnvironmentalEffects import getEnvEffects

application = Flask(__name__)
CORS(application)
api = Api(application)

# Initialize counter to download filename
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
    	latitudeString  = request.args.get('latitude')
    	longitudeString = request.args.get('longitude')
        dateString      = request.args.get('date')
        timeString      = request.args.get('time')
        param           = request.args.get('param')
        if not latitudeString or not longitudeString or not dateString or not timeString:
            raise BadRequest('Must pass latitude and longitude and a datetime')
        latitudeValue  = float(latitudeString)
        longitudeValue = float(longitudeString)
    	queryLocation  =  '%s,%s' %(latitudeString, longitudeString)
        
    	# Pass in a lat & long to the elevation query and get result
    	elevationQueryResponse = getElevation(queryLocation) # get the elevation according to the queried location
        if elevationQueryResponse is None:
            print "ELEVATION FAIL"
    	# Pass in a lat & long to the visible satellites query and get result
        visibleSatellites, satelliteDetails, constellationQuality = getVisibleGPSSatellites(latitudeValue, longitudeValue,
                                                                                            elevationQueryResponse, dateString, timeString)
        if visibleSatellites is None:
            print "VISIBLE SATELLITES FAIL"

        global counter
        if counter % 1000 == 0:
            downloadTLE()

        env = getEnvEffects(param)
        accuracy = env*constellationQuality

        # Compile JSON
        totalResponse = {'latitude':   latitudeString,
   		         'longitude':  longitudeString,
  		         'elevation':  elevationQueryResponse,
                         'date':       dateString,
                         'time':       timeString,
                         'satelliteDetails': satelliteDetails,
                         'numberVisibleSatellites': visibleSatellites,
                         'constellationQuality': constellationQuality,
                         'environment': env,
                         'accuracy': accuracy}

    	return totalResponse

        # Download the file if there have been at least X calls without a download
        counter += 1
        # print "counter is %d" % counter

api.add_resource(LeafletMap,'/')
api.add_resource(LocationAPI, '/data')
api.add_resource(Ping, '/ping')
api.add_resource(About, '/about')

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
