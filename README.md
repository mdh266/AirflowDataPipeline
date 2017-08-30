# Airflow Data Pipeline

This example walks through how to set up an ETL pipeline using <a href="https://airflow.incubator.apache.org/">Airflow</a>. I set up at DAG to query the <a href="https://openweathermap.org/">openweathermap.org</a> API everyday, process the json data and store it in a <a href="https://www.postgresql.org/">PostgreSQL</a> database.  For explanation of how this code works see this <a href="http://michael-harmon.com/blog/AirflowETL.html">blog post</a>

## Requirements

<a href="https://airflow.incubator.apache.org/">Airflow</a>

<a href="https://www.python.org/">Python 2.7</a>

<a href="https://www.postgresql.org/">PostgreSQL</a>

<a href="http://initd.org/psycopg/">psycopg</a>

<a href="https://www.sqlalchemy.org/">SQLAlchemy</a>

<a href="https://sqlalchemy-utils.readthedocs.io/en/latest/">SQLAlchemy-Utils</a>

To install the requirements (except for Python and postgres) type:

	pip install -r requirements.t
