from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator


default_args = {
				'owner' : 'Mike',
				'depends_on_past' :False,
				'email' :['mdh266@gmail.com'],
			    'email_on_failure': False,
			    'email_on_retry': False,
			    'retries': 5,
			    'retry_delay': timedelta(minutes=5)
				}


dag = DAG(
		  'FirstDag',
		  default_args=default_args,
		  start_date=datetime(2017,8,24,17,44),
		  schedule_interval=timedelta(minutes=1)
		  )


task1 = BashOperator(
 					task_id='make_a_file',
 					bash_command='touch ~/desktop/hello_world.txt',
 					dag=dag)

