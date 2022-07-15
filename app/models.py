import datetime
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.types import Date, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Production(Base):
    __tablename__ = 'productions'
    
    id = Column(Integer, primary_key=True, index=True)
    project = Column(String(254))  
    machine = Column(String(254)) # Machine producing pieces
    model = Column(String(254)) # Model of the piece produced by clip_machine
    shift_date = Column(Date) # Date of the shift recorded YYYY-mm-dd
    shift_time = Column(String(10)) # Hours in which the shift lasted
    quantity = Column(Integer, default=0) # Actual number of pieces produced during the shift
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.datetime.now())

    def to_dict(self):
      dict= { c.name: getattr(self, c.name) for c in self.__table__.columns}
      dict['shift_date']= dict['shift_date'].isoformat()

      return dict
class Defect(Base):
  __tablename__ ='defects'

  id = Column(Integer, primary_key=True, index=True)
  project = Column(String(254))
  model = Column(String)
  machine = Column(String)
  shift_date = Column(Date)
  shift_time = Column(String(10))
  reason = Column(String(254))
  quantity = Column(Integer)
  created_at = Column(DateTime, default=datetime.datetime.now())
  updated_at = Column(DateTime, onupdate=datetime.datetime.now())

  def to_dict(self):
    dict= { c.name: getattr(self, c.name) for c in self.__table__.columns}
    dict['shift_date']= dict['shift_date'].isoformat()
    return dict
class DownTime(Base):
  __tablename__ ='downtimes'

  id = Column(Integer, primary_key=True, index=True)
  project = Column(String(254))
  model = Column(String)
  machine = Column(String)
  shift_date = Column(Date)
  shift_time = Column(String(10))
  reason = Column(String(254))
  quantity = Column(Integer)
  created_at = Column(DateTime, default=datetime.datetime.now())
  updated_at = Column(DateTime, onupdate=datetime.datetime.now())

  def to_dict(self):
    dict= { c.name: getattr(self, c.name) for c in self.__table__.columns}
    dict['shift_date']= dict['shift_date'].isoformat()
    return dict  