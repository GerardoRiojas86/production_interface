from datetime import datetime
from flask import current_app
import pandas as pd

from ..models import  Project
from ..database import engine
from ..utils import Query


def get_projects():
  projects_query = Query(
    query=current_app.session.query(Project),
    conn=engine
  )

  return projects_query.to_df()
