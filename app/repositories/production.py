from datetime import datetime
from flask import current_app
import pandas as pd
import json 

from .. import  models
from ..database import engine

import random

SHIFT_HOURS = [
        "7:00",
        "8:00",
        "9:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00"
      ]

generate_hex_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF),range(n)))

class Query():

  def __init__(self, query=None, conn=None):
    self.query = query
    self.conn = conn
    pass
  
  def __get_data_frame__(self, as_dict=False):
    if (self.query != None and self.conn != None):
      df= pd.read_sql_query(
            sql= self.query,
            con=self.conn)

      if as_dict:
        return df.to_dict('records')

      else:
        return df

    else:
      return None

def production_exist(date, time, project_id):
  res= current_app.session.query(models.Production).filter_by(shift_date=date, shift_time=time, id=project_id).first()

  if res != None:
    return True
  else:
    return False

def get_hourly_production_data(date, project_id, project_rate, project_goal): 
  production_query = Query(
    query=current_app.session.query(models.Production).filter_by(shift_date=date, project_id=project_id).statement,
    conn=engine)

  production_df = production_query.__get_data_frame__()
  production_dict = production_df.to_dict('records')

  # production_reality_df = production_df[['shift_time', 'quantity']].groupby(['shift_time'], as_index=False).sum()

  
  hourly_production_rate = {}
  hourly_production_goal = {}
  hourly_production_reality = {}
  daily_production_reality = 0
  daily_production_goal = 0
  daily_production_rate = 0

  for shift_hour in SHIFT_HOURS:
    
    shift_hour_data = next((row for row in production_dict if row['shift_time'] == shift_hour), None)

    hourly_production_reality[shift_hour] = shift_hour_data['quantity'] if shift_hour_data else 0
    hourly_production_goal[shift_hour] = project_goal
    hourly_production_rate[shift_hour] = project_rate

    daily_production_reality += hourly_production_reality[shift_hour]
    daily_production_goal += project_goal
    daily_production_rate += project_rate

  return {
    "reality": {
      "label": "Reality",
      "color": "#CB1F39",
      "total": daily_production_reality,
      "data": list(hourly_production_reality.values())
    },

    "rate": {
      "label": "Rate",
      "color": "#060001",
      "total": daily_production_rate,
      "data": list(hourly_production_rate.values())
    },

    "goal": {
      "label": "Goal",
      "color": "#1FCB1F",
      "total": daily_production_goal,
      "data": list(hourly_production_goal.values())
    },
  }

def get_hourly_defect_data(date, project_id): 
  defect_query = Query(
    query=current_app.session.query(models.Defect).filter_by(shift_date=date, project_id=project_id).statement,
    conn=engine)

  defect_df = defect_query.__get_data_frame__()

  
  defect_df['timestamp'] = defect_df['shift_date'].astype(str) + " " + defect_df['shift_time'].astype(str)
  defect_df['timestamp'] = pd.to_datetime(defect_df['timestamp'], format='%Y-%m-%d %H:%M')

  defects_reasons_df = defect_df[['reason', 'quantity']].groupby(['reason']).sum()

  if defects_reasons_df.empty:
    defects_reasons_dict= {}
  else:
    defects_reasons_dict = defects_reasons_df.to_dict()['quantity']

  defect_resample = defect_df.resample('H', on='timestamp').quantity.sum()  

  defect_hourly_df = defect_resample.to_frame().reset_index()
  defect_hourly_df['timestamp'] = defect_hourly_df['timestamp'].dt.strftime('%-H:%M')

  defect_hourly_data = {}
  daily_total_defects = 0

  for hour in SHIFT_HOURS:
    res = defect_hourly_df.loc[ defect_hourly_df['timestamp'] == hour ]
    defect_hourly_data[hour] = int(res.iloc[0]['quantity']) if not res.empty else 0  
    daily_total_defects += defect_hourly_data[hour]

  return {
    "groups": {
      "colors": generate_hex_colors(len(defects_reasons_dict)),
      "labels": list(defects_reasons_dict.keys()),
      "values": list(defects_reasons_dict.values())
    },
    "total": daily_total_defects,
    "data": list(defect_hourly_data.values())
  }

def get_hourly_downtime_data(date, project_id): 
  downtime_query = Query(
    query=current_app.session.query(models.DownTime).filter_by(shift_date=date, project_id=project_id).statement,
    conn=engine)

  downtime_df = downtime_query.__get_data_frame__()

  
  downtime_df['timestamp'] = downtime_df['shift_date'].astype(str) + " " + downtime_df['shift_time'].astype(str)
  downtime_df['timestamp'] = pd.to_datetime(downtime_df['timestamp'], format='%Y-%m-%d %H:%M')

  downtime_reasons_df = downtime_df[['reason', 'quantity']].groupby(['reason']).sum()

  if downtime_reasons_df.empty:
    downtime_reasons_dict = {}
  else:
    downtime_reasons_dict = downtime_reasons_df.to_dict()['quantity']

  downtime_resample = downtime_df.resample('H', on='timestamp').quantity.sum()  

  downtime_hourly_df = downtime_resample.to_frame().reset_index()
  downtime_hourly_df['timestamp'] = downtime_hourly_df['timestamp'].dt.strftime('%-H:%M')

  downtime_hourly_data = {}
  daily_total_downtime = 0

  for hour in SHIFT_HOURS:
    res = downtime_hourly_df.loc[ downtime_hourly_df['timestamp'] == hour ]
    downtime_hourly_data[hour] = int(res.iloc[0]['quantity']) if not res.empty else 0  
    daily_total_downtime += downtime_hourly_data[hour]

  return {
    "groups": {
      "colors": generate_hex_colors(len(downtime_reasons_dict)),
      "labels": list(downtime_reasons_dict.keys()),
      "values": list(downtime_reasons_dict.values())
    },
    "total": daily_total_downtime,
    "data": list(downtime_hourly_data.values())
  }

def get_shift_data(shift_date, project_id, project_rate, project_goal):
  daily_production_data = get_hourly_production_data(shift_date, project_id, project_rate, project_goal)
  daily_defect_data = get_hourly_defect_data(shift_date, project_id)
  daily_downtime_data = get_hourly_downtime_data(shift_date, project_id)
  data = {}

  for index in range(len(SHIFT_HOURS)):
    hour = SHIFT_HOURS[index]
    
    data[hour] = {
      "reality": daily_production_data['reality']['data'][index],
      "defects": daily_defect_data['data'][index],
      "downtime": daily_downtime_data['data'][index]
    }

  return {
    "date": shift_date,
    "hours": SHIFT_HOURS,
    "production": daily_production_data,
    "defects": daily_defect_data,
    "downtimes": daily_downtime_data,
    "colors": generate_hex_colors(len(SHIFT_HOURS)),
    "total": {
      "production": {
        "reality": daily_production_data['reality']['total'],
        "rate": daily_production_data['rate']['total'],
        "goal": daily_production_data['goal']['total']
      },
      "defects": daily_defect_data['total'],
      "downtime": daily_downtime_data['total']
    },
    "data": data
  }