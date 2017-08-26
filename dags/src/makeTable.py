from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

def make_database():
    """
    Make the Postgres database and create the table.
    """

	dbname    = 'WeatherDB'
	username  = 'Mike'
	tablename = 'weather_table'

    # Note: I didn't make a password.
	engine    = create_engine('postgresql+psycopg2://%s@localhost/%s'%(username,dbname))

	if not database_exists(engine.url):
   		create_database(engine.url)

	conn = psycopg2.connect(database = dbname, user = username)

	curr = conn.cursor()

	create_table = """CREATE TABLE IF NOT EXISTS %s
                (
                    city         TEXT, 
                    country      TEXT,
                    latitude     REAL,
                    longitude    REAL,
                    todays_date  DATE,
                    humudity     REAL,
                    pressure     REAL,
                    min_temp     REAL,
                    max_temp     REAL,
                    temp         REAL,
                    weather      TEXT
                )
                """ % tablename

	curr.execute(create_table)
	conn.commit()
	conn.close()

if __name__ == "__main__":
	make_database()