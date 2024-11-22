from fastapi import APIRouter

router = APIRouter(prefix='/crimes')

@router.get('/numbers')
async def root():
    return { 'message': 'Testing' }
