import os
import dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load environment variables from .env
dotenv.load_dotenv()

# Build database URL
DATABASE_URL = f'''postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}'''

# SQLAlchemy Engine
engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=20)

# ORM models base
Base = declarative_base()

# SessionFactory
Session = sessionmaker(autocommit=False, bind=engine)

def init_db():
    # Create the tables in the database
    Base.metadata.create_all(bind=engine)

def query_total_crimes_by_year(year: int, conn):
    sql = f'''SELECT COUNT(year) from crimes
          WHERE year = {year};'''
    cur = conn.cursor()
    cur.execute(sql)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count

def is_table_empty(table_class):
    session = Session()
    try:
        return not session.query(table_class).first()
    except sqlalchemy.exc.ProgrammingError:
        # Handle case where the table does not exist
        return True
    finally:
        session.close()

