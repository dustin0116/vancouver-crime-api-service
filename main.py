'''
main.py
-------

This is the main module that runs the FastAPI backend service.

Dependencies:
-------------
- logging: Used for SQLAlchemy logging.
- asynccontextmanager: Used for the service's startup and shutdown tasks.
- FastAPI: Used to run app as a FastAPI service.
- CORSMiddleware: Used to set up the CORS Middleware
- process: Used to run the data initialization process for the crime source data.
- init_db: Used to initialize the crimes table for the database.
- is_table_empty: Used to check if a table is empty.
- load_csv_data: Used to load csv data into the database.
- Crime: The ORM Model Class for crimes.
- crimes: The crimes API route.
'''
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.pool import init_db
from .database.utilities import is_table_empty, load_csv_data
from .models.crime_orm import Crime
from .routers import crimes

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)  # Logs SQL statements

@asynccontextmanager
async def lifespan(_: FastAPI):
    ''' Startup of the service initializes the table and processes the csv data. '''
    logging.info("Initializing database...")
    init_db()
    if is_table_empty(Crime):
        logging.info("Crime table is empty. Populating data...")
        load_csv_data()
    else:
        logging.info("Crime table already populated.")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(crimes.router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
