from sqlalchemy import Column, String, Date, CHAR, TIMESTAMP, Integer
from ...db.base_class import Base
import datetime

class Event(Base):
    __tablename__ = 'events'
    __table_args__ = {"schema": "public"}
    event_id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    name = Column(String, nullable=True)
    location = Column(String, nullable=True)
    start_time = Column(TIMESTAMP, nullable=True)
    end_time = Column(TIMESTAMP)
    max_capacity = Column(Integer, nullable=True)


    