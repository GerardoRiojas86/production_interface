import datetime
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.types import Date, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Projects(Base):
  __tablename__ = 'projects'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(254))
  plant = Column(String(254))
  models = relationship('Model', backref='projects', lazy='select')

class Model(Base):
  __tablename__ = 'models'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(254))
  description = Column(String(254))
  project_id = Column(Integer, ForeignKey('projects.id'))

class Production(Base):
    __tablename__ = 'productions'
    
    id = Column(Integer, primary_key=True, index=True)
    project = Column(String(254))  
    machine = Column(String(254)) # Machine producing pieces
    model = Column(String(254)) # Model of the piece produced by clip_machine
    shift_date = Column(Date) # Date of the shift recorded YYYY-mm-dd
    shift_time = Column(Integer) # Hours in which the shift lasted
    goal = Column(Integer, default=0) # Expected number of pieces to  be produced during the shift
    rate = Column(Integer, default=0) # Rate of pieces the machine can produce
    quantity = Column(Integer, default=0) # Actual number of pieces produced during the shift
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.datetime.now())

class Defect(Base):
  __tablename__ ='defects'

  id = Column(Integer, primary_key=True, index=True)
  project = Column(String(254))
  model = Column(String)
  machine = Column(String)
  shift_date = Column(Date)
  shift_time = Column(Integer)
  reason = Column(String(254))
  quantity = Column(Integer)
  created_at = Column(DateTime, default=datetime.datetime.now())
  updated_at = Column(DateTime, onupdate=datetime.datetime.now())


class DownTime(Base):
  __tablename__ ='downtimes'

  id = Column(Integer, primary_key=True, index=True)
  project = Column(String(254))
  model = Column(String)
  machine = Column(String)
  shift_date = Column(Date)
  shift_time = Column(Integer)
  reason = Column(String(254))
  quantity = Column(Integer)
  created_at = Column(DateTime, default=datetime.datetime.now())
  updated_at = Column(DateTime, onupdate=datetime.datetime.now())