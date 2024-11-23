from fastapi import APIRouter
router = APIRouter(prefix='/crimes')

@router.get('/total-crimes-{year}')
async def read_total_crimes_by_year(year: int):
    return { 'message': 'Hi' }
