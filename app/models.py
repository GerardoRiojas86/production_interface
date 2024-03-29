import datetime
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.types import Date, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Project(Base):
  __tablename__ = 'projects'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(254))
  models = relationship('Model', backref='projects', lazy='select')
  machines = relationship('Machine', backref='projects', lazy='select')
  reasons = relationship('Reason', backref='reasons', lazy='select')
  rate = Column(Integer, default=0)
  goal = Column(Integer, default=0)

  created_at = Column(DateTime, default=datetime.datetime.now())
  updated_at = Column(DateTime, onupdate=datetime.datetime.now())

  def to_dict(self):
    dict= { c.name: getattr(self, c.name) for c in self.__table__.columns}
    dict['created_at'] = dict['created_at'].isoformat() if dict['created_at'] else ''
    dict['updated_at'] = dict['updated_at'].isoformat() if dict['updated_at'] else ''
    dict['models'] = [model.to_dict() for model in self.models]
    dict['machines'] = [machine.to_dict() for machine in self.machines]
    dict['reasons'] = [reason.to_dict() for reason in self.reasons]

    return dict

class Model(Base):
  __tablename__ = 'models'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(254))
  project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)

  created_at = Column(DateTime, default=datetime.datetime.now())
  updated_at = Column(DateTime, onupdate=datetime.datetime.now())  

  def to_dict(self):
    dict= { c.name: getattr(self, c.name) for c in self.__table__.columns}
    dict['created_at'] = dict['created_at'].isoformat() if dict['created_at'] else ''
    dict['updated_at'] = dict['updated_at'].isoformat() if dict['updated_at'] else ''

    return dict  

class Machine(Base):
  __tablename__ = 'machines'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(254))
  project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)

  created_at = Column(DateTime, default=datetime.datetime.now())
  updated_at = Column(DateTime, onupdate=datetime.datetime.now())  

  def to_dict(self):
    dict= { c.name: getattr(self, c.name) for c in self.__table__.columns}
    dict['created_at'] = dict['created_at'].isoformat() if dict['created_at'] else ''
    dict['updated_at'] = dict['updated_at'].isoformat() if dict['updated_at'] else ''

    return dict  


class Reason(Base):
  __tablename__ = 'reasons'

  id = Column(Integer, primary_key=True, index=True)
  description = Column(String(500))
  category = Column(String(10)) # defect, downtime
  project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)

  created_at = Column(DateTime, default=datetime.datetime.now())
  updated_at = Column(DateTime, onupdate=datetime.datetime.now())  

  def to_dict(self):
    dict= { c.name: getattr(self, c.name) for c in self.__table__.columns}
    dict['created_at'] = dict['created_at'].isoformat() if dict['created_at'] else ''
    dict['updated_at'] = dict['updated_at'].isoformat() if dict['updated_at'] else ''

    return dict

class Production(Base):
  __tablename__ = 'productions'
  
  id = Column(Integer, primary_key=True, index=True)
  machine = Column(String(254)) # Machine producing pieces
  model = Column(String(254)) # Model of the piece produced by clip_machine
  shift_date = Column(Date) # Date of the shift recorded YYYY-mm-dd
  shift_time = Column(String(10)) # Hours in which the shift lasted
  quantity = Column(Integer, default=0) # Actual number of pieces produced during the shift
  project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)

  created_at = Column(DateTime, default=datetime.datetime.now())
  updated_at = Column(DateTime, onupdate=datetime.datetime.now())

  def to_dict(self):
    dict= { c.name: getattr(self, c.name) for c in self.__table__.columns}
    dict['shift_date']= dict['shift_date'].isoformat()
    dict['created_at'] = dict['created_at'].isoformat() if dict['created_at'] else ''
    dict['updated_at'] = dict['updated_at'].isoformat() if dict['updated_at'] else ''

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
  project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)

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
  project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)

  created_at = Column(DateTime, default=datetime.datetime.now())
  updated_at = Column(DateTime, onupdate=datetime.datetime.now())

  def to_dict(self):
    dict= { c.name: getattr(self, c.name) for c in self.__table__.columns}
    dict['shift_date']= dict['shift_date'].isoformat()
    return dict  