from fastapi import FastAPI
from .routers import crimes
from .database import database

database.initialize_crimes()

app = FastAPI()

app.include_router(crimes.router)
