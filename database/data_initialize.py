import csv
from .models import Crimes
from .db_pool import Session
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

def process():
    session = Session()
    with open ('data/crimedata_csv_AllNeighbourhoods_AllYears.csv', 'r') as f:
        reader = csv.DictReader(f)
        entries = []
        # Prepare table entries
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
            # Insert table entries`
            session.add_all(entries)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f'An error occurred: {e}')
        finally:
            session.close()
