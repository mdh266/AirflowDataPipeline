import requests
import config as C 
import json
from datetime import datetime 
import os

def get_weather():

	paramaters = {'q': 'Paris,fr', 'appid':C.API_KEY}

	result     = requests.get("http://api.openweathermap.org/data/2.5/weather?", paramaters)

	if result.status_code == 200 :

		json_data = result.json()

		file_name  = str(datetime.now().replace(microsecond=0)).replace(' ','T') + '.json'
		tot_name   = os.path.join(os.path.dirname(__file__), 'unprocessed', file_name)

		print tot_name

		with open(tot_name, 'w') as outputfile:
			json.dump(json_data, outputfile)
	else :
		print "Error"


if __name__ == "__main__":
	get_weather()
