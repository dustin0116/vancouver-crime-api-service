'''
db_pool.py
----------

This module sets up the database connection pool.

Dependencies:
-------------
- os: Used for retrieving environment variables.
- dotenv: Used to load environment variables from .env 
- SQLAlchemy: Used to set up ORM Base model and Session.
'''
import os

import dotenv
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env
dotenv.load_dotenv()

# Build database URL
DATABASE_URL = (
    f'''postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}''' +
    f'''@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}'''
)
# SQLAlchemy Engine
engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=20)

# ORM models base
Base = declarative_base()

# SessionFactory
Session = sessionmaker(autocommit=False, bind=engine)

def init_db():
    ''' Initializes the crimes table in the database '''
    Base.metadata.create_all(bind=engine)
