
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.types import Date
from .database import Base


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    days = Column(Integer, default=0)
    clip_machine = Column(String(254))
    model = Column(String(254))
    hours = Column(Integer)
    goal = Column(String(254))
    rate = Column(Float)
    reality = Column(Float)
    defects = Column(String(254))
    defects_qty = Column(Integer)
    down_time = Column(Integer)
    down_time_qty = Column(Integer)