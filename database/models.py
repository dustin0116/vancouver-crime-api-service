from .db_pool import Base
from sqlalchemy import Column, Integer, String, DateTime

def test():
    print('test')
class Crimes(Base):
    __tablename__ = 'crimes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    case = Column(String)
    event_datetime = Column(DateTime)
    hundred_block = Column(String)
    neighborhood = Column(String)
    x = Column(String)
    y = Column(String)
