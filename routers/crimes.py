'''
crimes.py
---------

This is the module that sets the APIs.

Dependencies:
-------------
- APIRouter: Set the API URL route.
'''
import logging

from fastapi import APIRouter
from sqlalchemy import extract

from ..database.pool import Session
from ..models.crime_orm import Crime

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)  # Logs SQL statements

router = APIRouter(prefix='/crimes')

@router.get('/total')
async def read_total_crimes(year: int):
    ''' Returns the total number of crimes. '''
    # session = Session()
    # # Query unique years
    # years = session.query(extract('year', Crime.event_datetime)).distinct().all()
    # years = [year[0] for year in years]
    return { 'total': year }

@router.get('/all_years')
async def read_all_years():
    ''' Returns the years of the dataset. '''
    session = Session()
    # Query unique years
    years = session.query(extract('year', Crime.event_datetime)).distinct().all()
    logging.info(years)
    years = [year[0] for year in years]
    return { 'years': years }
