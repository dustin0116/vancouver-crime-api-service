'''
crimes.py
---------

This is the module that sets the APIs.

Dependencies:
-------------
- APIRouter: Set the API URL route.
'''
from fastapi import APIRouter

router = APIRouter(prefix='/crimes')

@router.get('/total-crimes-{year}')
async def read_total_crimes_by_year(year: int):
    '''Returns the total number of crimes in the specified year'''
    return { 'message': year }
