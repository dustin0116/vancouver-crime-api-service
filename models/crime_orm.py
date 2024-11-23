'''
crime_orm.py
---------

This module contains utility functions and ORM model for the crimes table

Dependencies:
-------------
- SQLAlchemy: Used for ORM mapping.
- Base: Used for SQLAlchemy model registry.
'''
from sqlalchemy import Column, DateTime, Integer, String

from ..database.db_pool import Base


class Crime(Base):
    '''
    Represents a crime event from the database.

    Attributes:
        id (int): Unique ID for the crime event. Primary Key.
        case (str): The type of crime committed.
        event_datetime (datetime): The time (YYYY/MM/DD HH:MM) the crime occurred.
        hundred_b
        neighborhood (str): The neighborhood where the crime occurred.
        x (str): The X coordinates of the crime.
        y (str): The Y coordinates of the crime.
    '''
    __tablename__ = 'crimes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    case = Column(String)
    event_datetime = Column(DateTime)
    hundred_block = Column(String)
    neighborhood = Column(String)
    x = Column(String)
    y = Column(String)

    def get_event_datetime(self):
        ''' Get Date and Time. '''
        return self.event_datetime

    def get_coordinates(self):
        ''' Get coordinates of the crime. '''
        return self.x, self.y
