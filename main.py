import logging
from fastapi import FastAPI
from .routers import crimes
from .database.db_pool import init_db, process

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)  # Logs SQL statements

app = FastAPI()



@app.on_event("startup")
async def startup_event():
    init_db()
    process()


app.include_router(crimes.router)