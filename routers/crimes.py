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

@router.get('/total')
async def read_total_crimes(year: int):
    ''' Returns the total number of crimes. '''
    return { 'message': year }
