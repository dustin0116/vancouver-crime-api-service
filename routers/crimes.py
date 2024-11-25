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
import logging

from fastapi import APIRouter, HTTPException
from sqlalchemy import extract, select
from sqlalchemy.exc import SQLAlchemyError

from ..database.pool import Session
from ..models.crime_orm import Crime

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)  # Logs SQL statements

router = APIRouter()

@router.get('/years')
async def read_all_years():
    ''' Returns the years of the dataset. '''
    session = Session()
    # Query unique years
    try:
        years = session.query(extract('year', Crime.event_datetime)).distinct().all()
        if not years:
            raise HTTPException(status_code=404, detail="Years not found in database")
        years = [year[0] for year in years]
        return { 'years': years }
    except SQLAlchemyError as e:
        print(f'An error occurred: {e}')
        raise HTTPException(status_code=500, detail="Database error occurred") from e
    finally:
        session.close()

@router.get('/crimes')
async def read_all_crimes(year: int):
    ''' Returns all of the crimes within the specified year in the database. '''
    session = Session()
    # Query unique years
    try:
        all_crimes = session.execute(select(Crime).where(Crime.event_datetime == year))
        return all_crimes
    except SQLAlchemyError as e:
        print(f'An error occurred: {e}')
        raise HTTPException(status_code=500, detail="Database error occurred") from e
    finally:
        session.close()
