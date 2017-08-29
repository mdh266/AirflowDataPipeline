from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators import PythonOperator
import os
from airflow.hooks import PostgresHook
import json
import numpy as np


def load_data(ds, **kwargs):
	"""
	Processes the json data, checks the types and enters into the
	Postgres database.
	"""

	pg_hook  = PostgresHook(postgres_conn_id='weather_id')

	file_name = str(datetime.now().date()) + '.json'
	tot_name = os.path.join(os.path.dirname(__file__),'src/data', file_name)

	# open the json datafile and read it in
	with open(tot_name, 'r') as inputfile:
		doc = json.load(inputfile)

	# transform the data to the correct types and convert temp to celsius
	city        = str(doc['name'])
	country     = str(doc['sys']['country'])
	lat         = float(doc['coord']['lat'])
	lon         = float(doc['coord']['lon'])
	humid       = float(doc['main']['humidity'])
	press       = float(doc['main']['pressure'])
	min_temp    = float(doc['main']['temp_min']) - 273.15
	max_temp    = float(doc['main']['temp_max']) - 273.15
	temp        = float(doc['main']['temp']) - 273.15
	weather     = str(doc['weather'][0]['description'])
	todays_date = datetime.now().date()

	# check for nan's in the numeric values and then enter into the database
	valid_data  = True
	for valid in np.isnan([lat, lon, humid, press, min_temp, max_temp, temp]):
		if valid is False:
			valid_data = False
			break;

	row  =  (city, country, lat, lon, todays_date, humid, press, min_temp,
			max_temp, temp, weather)

	insert_cmd = """INSERT INTO weather_table 
					(city, country, latitude, longitude,
					todays_date, humidity, pressure, 
					min_temp, max_temp, temp, weather)
					VALUES
					(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

	if valid_data is True:
		pg_hook.run(insert_cmd, parameters=row)


# Define the default dag arguments.
default_args = {
		'owner' : 'Mike',
		'depends_on_past' :False,
		'email' :['mdh266@gmail.com'],
		'email_on_failure': False,
		'email_on_retry': False,
		'retries': 5,
		'retry_delay': timedelta(minutes=1)
		}


# Define the dag, the start date and how frequently it runs.
# I chose the dag to run everday by using 1440 minutes.
dag = DAG(
		dag_id='weatherDag',
		default_args=default_args,
		start_date=datetime(2017,8,24),
		schedule_interval=timedelta(minutes=1440))


# First task is to query get the weather from openweathermap.org.
task1 = BashOperator(
			task_id='get_weather',
			bash_command='python ~/airflow/dags/src/getWeather.py' ,
			dag=dag)


# Second task is to process the data and load into the database.
task2 =  PythonOperator(
			task_id='transform_load',
			provide_context=True,
			python_callable=load_data,
			dag=dag)

# Set task1 "upstream" of task2, i.e. task1 must be completed
# before task2 can be started.
task1 >> task2 

