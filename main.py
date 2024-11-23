import logging
from fastapi import FastAPI
from .routers import crimes
from .database.db_pool import init_db, is_table_empty
from .database.data_initialize import process
from .database.models import Crimes
from contextlib import asynccontextmanager

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)  # Logs SQL statements


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Initializing database...")
    init_db()
    if is_table_empty(Crimes):
        logging.info("Crimes table is empty. Populating data...")
        process()
    else:
        logging.info("Crimes table already populated.")
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(crimes.router)
