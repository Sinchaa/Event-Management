from sqlalchemy import Column, String, Date, CHAR, TIMESTAMP, Integer
from ...db.base_class import Base
import datetime
from sqlalchemy import ForeignKey

class Attendee(Base):
    __tablename__ = 'attendees'
    __table_args__ = {"schema": "public"}
    event_id = Column(Integer, ForeignKey('public.events.event_id'), primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, primary_key=True, nullable=True)


    