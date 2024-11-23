import logging
from fastapi import FastAPI
from .routers import crimes
from .database.db_pool import init_db, process

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)  # Logs SQL statements

init_db()
#process()

app = FastAPI()

app.include_router(crimes.router)
