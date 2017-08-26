from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators import PythonOperator
import os
from airflow.hooks import PostgresHook


SRC_DIR = os.getcwd() + '/src/'


def get_rates(ds, **kwargs):
	pg_hook = PostgresHook(postgres_conn_id='birth_db')

	print pg_hook.get_records("SELECT * FROM birth_data_table limit 1")

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



task2 =  PythonOperator(task_id='get_rates',
	                   provide_context=True,
	                   python_callable=get_rates,
	                   dag=dag)


task1 >> task2 

