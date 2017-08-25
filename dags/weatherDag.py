from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
import os


SRC_DIR = os.getcwd() + '/src/'

default_args = {
				'owner' : 'Mike',
				'depends_on_past' :False,
				'email' :['mdh266@gmail.com'],
			    'email_on_failure': False,
			    'email_on_retry': False,
			    'retries': 5,
			    'retry_delay': timedelta(minutes=1)
				}


dag = DAG(
		  'weatherDag',
		  default_args=default_args,
		  start_date=datetime(2017,8,24)#,
		  #schedule_interval=timedelta(minutes=1)
		  )


task1 = BashOperator(
 					task_id='get_weather',
 					bash_command='python ~/airflow/dags/src/getWeather.py' ,
 					dag=dag)

