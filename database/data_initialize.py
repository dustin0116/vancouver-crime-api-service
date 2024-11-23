'''
data_initialize.py
------------------

This module loads the crime data from the csv source to the database.

Dependencies:
-------------
- csv: Used for reading csv source file.
- datetime: Used for converting source data's date to one single datetime value
- SQLAlchemy: Used for checking database process errors.
- Session: Used for opening a session for database writing
- Crimes: The ORM Model Class for Crimes
'''
import csv
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from .db_pool import Session
from .models import Crimes


def process():
    '''Process the source csv dataset to the database'''
    session = Session()
    with open(
        'sourcedata/crimedata_csv_AllNeighbourhoods_AllYears.csv',
        'r',
        encoding='utf-8'
    ) as f:
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

def is_crimes_table_empty():
    session = Session()
    try:
        return not session.query(Crimes).first()
    finally:
        session.close()
