#!flask/bin/python
from flask import Flask
from flask import abort
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

#Get speed and distance reading
@app.route('/sensor', methods=['POST'])
def postBikeData():
	jsonDict = request.get_json()
	print jsonDict
	#Throw error if data not included
	if not jsonDict or not 'speed' in jsonDict or not 'distance' in jsonDict or not 'bikeid' in jsonDict:
		abort(400)

	print "SPEED", jsonDict['speed'], "DISTANCE", jsonDict['distance'], "BIKE_ID", jsonDict['bikeid']
	return 'ok', 200
	
if __name__ == '__main__':
    app.run(debug=True)

