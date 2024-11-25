'''
crimes.py
---------

This is the module that sets the APIs.

Dependencies:
-------------
- APIRouter: Set the API URL route.
- HTTPException: For raising HTTP errors.
- SQLAlchemy: For extracting query results and error checking.
- Session: Used for opening a session for database writing.
- Crime: The ORM Model Class for crimes.
'''
import json
import logging
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import extract, select

from ..database.pool import Session
from ..models.crime_orm import Crime

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)  # Logs SQL statements

router = APIRouter()
session = Session()

def crime_json(crime):
    ''' Get JSON of a crime '''
    print(crime.id)
    return {
        'id': crime.id,
        'case': crime.case,
        'date': crime.event_datetime.isoformat(),
        'address': crime.hundred_block,
        'neighborhood': crime.neighborhood,
        'x': crime.x,
        'y': crime.y
    }

@router.get('/years')
async def read_all_years():
    ''' Returns the years of the dataset. '''
    with session.begin():
    # Get distinct years
        result = session.execute(select(extract('year', Crime.event_datetime)).distinct())
        distinct_years = [row[0] for row in result]
        distinct_years = ([ int(year)
                            if isinstance(year, Decimal)
                            else year for year in distinct_years
                         ])

        return JSONResponse(content={'years': distinct_years})

@router.get('/crimes/{year}')
async def read_all_crimes(year: int):
    ''' Returns all of the crimes within the specified year in the database. '''
    with session.begin():
        start_date = datetime(year, 1, 1)
        end_date = datetime(year+1, 1, 1)
        query = ( select(Crime)
                 .where(Crime.event_datetime >= start_date)
                 .where(Crime.event_datetime < end_date)
                )
        result = session.execute(query).all()
        crimes = [crime_json(crime[0]) for crime in result]  # Convert each row to dict
        return JSONResponse(content=crimes)
