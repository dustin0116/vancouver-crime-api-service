import os
import csv
import dotenv
import sqlalchemy
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base

# Load environment variables from .env
dotenv.load_dotenv()

# Build database URL
DATABASE_URL = f'''postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}'''

print(DATABASE_URL)
# SQLAlchemy Engine
engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=20)

# ORM models base
Base = declarative_base()

# SessionFactory
Session = sessionmaker(autocommit=False, bind=engine)

def init_db():
    # Create the tables in the database
    Base.metadata.create_all(bind=engine)

def query_total_crimes_by_year(year: int, conn):
    sql = f'''SELECT COUNT(year) from crimes
          WHERE year = {year};'''
    cur = conn.cursor()
    cur.execute(sql)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count

def process():
    from .models import Crimes
    session = Session()
    with open ('data/crimedata_csv_AllNeighbourhoods_AllYears.csv', 'r') as f:
        reader = csv.DictReader(f)
        entries = []
        for row in reader:
            # Combine the columns into a single datetime object
            year = int(row['YEAR'])
            month = int(row['MONTH'])
            day = int(row['DAY'])
            hour = int(row['HOUR'])
            minute = int(row['MINUTE'])
            event_datetime = datetime(year, month, day, hour, minute)
            row_data = Crimes(
                case = row['TYPE'],
                event_datetime = event_datetime,
                hundred_block = row['HUNDRED_BLOCK'],
                neighborhood = row['NEIGHBOURHOOD'],
                x = row['X'],
                y = row['Y']
            )
            entries.append(row_data)
        try:
            session.add_all(entries)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f'An error occurred: {e}')
        finally:
            session.close()
