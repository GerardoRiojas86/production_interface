from datetime import datetime
from flask import current_app
import pandas as pd

from ..models import  Project, Model, Machine, Reason
from ..database import engine
from ..utils import Query


def project_exist(name):
  project = current_app.session.query(Project).filter_by(name=name).first()

  if project:
    return True
  else:
    return False

def add_project(name, rate, goal):
  project = Project(
    name=name,
    rate=rate,
    goal=goal
  )

  current_app.session.add(project)
  current_app.session.commit()

  return project.to_dict()

def add_project_model(name, project_id):
  model = Model(
    name=name,
    project_id=project_id
  )

  current_app.session.add(model)
  current_app.session.commit()

  return model.to_dict()

def add_project_machine(name, project_id):
  machine = Machine(
    name=name,
    project_id=project_id
  )

  current_app.session.add(machine)
  current_app.session.commit()

  return machine.to_dict()

def add_project_reason(description, category, project_id):
  reason = Reason(
    description=description,
    category=category,
    project_id=project_id
  )

  current_app.session.add(reason)
  current_app.session.commit()

  return reason.to_dict()

def get_project_reasons(project_id, category):
  reasons = current_app.session.query(Reason).filter_by(project_id=project_id, category=category).all()

  return [reason.to_dict() for reason in reasons]

def get_project_machines(project_id):
  machines = current_app.session.query(Machine).filter_by(project_id=project_id).all()

  return [machine.to_dict() for machine in machines]


def get_project_models(project_id):
  models = current_app.session.query(Model).filter_by(project_id=project_id).all()

  return [model.to_dict() for model in models]

def get_projects():
  projects_query = Query(
    query=current_app.session.query(Project),
    conn=engine
  )

  projects_df = projects_query.to_df()
  del projects_df['created_at']
  del projects_df['updated_at']

  return projects_df.to_dict('records')


def get_project_by_id(id):
  project = current_app.session.query(Project).filter_by(id=id).first()

  if project:
    return project.to_dict()
  
  else:
    return None