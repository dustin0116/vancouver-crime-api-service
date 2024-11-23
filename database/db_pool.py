import os
import dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load environment variables from .env
dotenv.load_dotenv()

# Build database URL
DATABASE_URL = f'''postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}'''

print(DATABASE_URL)
# SQLAlchemy Engine
engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=20)

# ORM models base
Base = declarative_base()

# SessionFactory
Session = sessionmaker(autocommit=False, bind=engine)

def init_db():
    # Create the tables in the database
    Base.metadata.create_all(bind=engine)

