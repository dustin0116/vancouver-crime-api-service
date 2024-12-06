"""
utilities.py
------------

This module includes all utilities and data processing actions to the database.

Dependencies:
-------------
- csv: Used for reading csv source file.
- datetime: Used for converting source data's date to one single datetime value.
- SQLAlchemy: Used for checking database process errors.
- Session: Used for opening a session for database writing.
- Crime: The ORM Model Class for crimes.
"""

import csv
from datetime import datetime

from sqlalchemy import select

from ..models.crime_orm import Crime
from .pool import SessionLocal

session = SessionLocal()


def load_csv_data():
    """Process the source csv dataset to the database."""
    with session.begin():
        with open(
            "sourcedata/crimedata_csv_AllNeighbourhoods_AllYears.csv",
            "r",
            encoding="utf-8",
        ) as f:
            reader = csv.DictReader(f)
            entries = []
            for row in reader:
                year = int(row["YEAR"])
                month = int(row["MONTH"])
                day = int(row["DAY"])
                hour = int(row["HOUR"])
                minute = int(row["MINUTE"])
                event_datetime = datetime(year, month, day, hour, minute)
                row_data = Crime(
                    case=row["TYPE"],
                    event_datetime=event_datetime,
                    hundred_block=row["HUNDRED_BLOCK"],
                    neighborhood=row["NEIGHBOURHOOD"],
                    x=row["X"],
                    y=row["Y"],
                )
                entries.append(row_data)
            session.add_all(entries)


def is_table_empty(table_class):
    """
    Check if table is empty.

    Args:
        table_class (class): The ORM model class.
    """
    with session.begin():
        result = session.execute(select(table_class).limit(1)).fetchone() is not None
        return not result
