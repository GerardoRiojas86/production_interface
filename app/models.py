import datetime
from email.policy import default
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.types import Date, DateTime
from .database import Base

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    shift_date = Column(Date) # Date of the shift recorded YYYY-mm-dd
    shift_hours = Column(Integer) # Hours in which the shift lasted
    clip_machine = Column(String(254)) # Machine producing pieces
    model = Column(String(254)) # Model of the piece produced by clip_machine
    goal = Column(Integer, default=0) # Expected number of pieces to  be produced during the shift
    rate = Column(Integer, default=0) # Rate of pieces the machine can produce
    reality = Column(Integer, default=0) # Actual number of pieces produced during the shift
    defects = Column(String(254)) # Defect root cause
    defects_qty = Column(Integer, default=0) # Number of defected pieces 
    down_time_reason = Column(String(254)) # Reason of downtime
    down_time_qty = Column(Integer, default=0) # Minutes of no production 
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.datetime.now())