'''
main.py
-------

This is the main module that runs the FastAPI backend service.

Dependencies:
-------------
- logging: Used for SQLAlchemy logging.
- asynccontextmanager: Used for the service's startup and shutdown tasks.
- FastAPI: Used to run app as a FastAPI service.
- process: Used to run the data initialization process for the crime source data.
- init_db: Used to initialize the crimes table for the database.
- Crime: The ORM Model Class for crimes.
- crimes: Used to set up ORM Base model and Session.
'''
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database.data_initialize import is_table_empty, process
from .database.db_pool import init_db
from .database.models import Crime
from .routers import crimes

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)  # Logs SQL statements

@asynccontextmanager
async def lifespan(_: FastAPI):
    ''' Startup of the service initializes the table and processes the csv data. '''
    logging.info("Initializing database...")
    init_db()
    if is_table_empty(Crime):
        logging.info("Crime table is empty. Populating data...")
        process()
    else:
        logging.info("Crime table already populated.")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(crimes.router)
