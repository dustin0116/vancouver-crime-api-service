import psycopg2
from configparser import ConfigParser

def config(filename='database/database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db={}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

def initialize_crimes():
    conn = None
    try:
        params = config()
        print('Connecting to the database server...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # Creating table to store csv data
        sql = '''CREATE TABLE IF NOT EXISTS crimes (type VARCHAR(150),\
              year INT,\
              month INT,\
              day INT,\
              hour INT,\
              minute INT,\
              hundred_block CHAR(100),\
              neighborhood CHAR(100),\
              x VARCHAR(100),\
              y VARCHAR(100));
              '''
        cur.execute(sql)
        process(cur)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def process(cur):
    with open ('data/crimedata_csv_AllNeighbourhoods_AllYears.csv', 'r') as f:
        # Skip header row
        next(f)
        # Copy to crimes table
        cur.copy_from(f, 'crimes', sep=',')
