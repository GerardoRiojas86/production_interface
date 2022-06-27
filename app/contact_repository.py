from datetime import datetime
from turtle import down
from flask import current_app
import pandas as pd
import json 

from . import  models
from .database import engine

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
        "18:00",
        "19:00",
      ]


generate_hex_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF),range(n)))


class DayShift():

  def __init__(self, current_date, hours=[], query=None, conn=None):
    self.shift_hours = hours
    self.current_date = datetime.strptime(current_date,'%Y-%m-%d').date()
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
  
  def get_day_shift_table(self):
    day_shift_df = self.__get_data_frame__()

    if day_shift_df.empty:
      return {
        "hours": self.shift_hours,
        "date": self.current_date.isoformat(),
        "data": day_shift_df.to_dict('records'),
        "downtime": {},
        "defects": {}
      }

    else:
      day_shift_table = {}
      day_rates_table = {}
      day_goals_table = {}
      day_reality_table = {}

      day_shift_df['shift_date'] = day_shift_df['shift_date'].apply(
        lambda x: x.isoformat()
      )

      day_shift_df['created_at'] = day_shift_df['created_at'].apply(
        lambda x: x.isoformat()
      )


      day_shift_df['updated_at'] = day_shift_df['updated_at'].apply(
        lambda x: x.isoformat() if x != None else ''
      )

      day_shift_dict = day_shift_df.to_dict('records')

      for shift_hour in self.shift_hours:
        # shift_hour_data = [x for x in day_shift_dict if x['shift_hours'] == shift_hour]       
        # shift_hour_data = filter(lambda row: row['shift_hours'] == shift_hour, day_shift_dict)
        shift_hour_data = next((row for row in day_shift_dict if row['shift_hours'] == shift_hour), None)

        if shift_hour_data != None:
          day_shift_table[shift_hour] = shift_hour_data
          day_rates_table[shift_hour] = shift_hour_data['rate']
          day_goals_table[shift_hour] = shift_hour_data['goal']
          day_reality_table[shift_hour] = shift_hour_data['reality']
        else:
          day_shift_table[shift_hour] = {}
          day_rates_table[shift_hour] = 0
          day_goals_table[shift_hour] = 0
          day_reality_table[shift_hour] = 0
      

      # Calculate downtime aggregations for day shift
      down_time_agg = day_shift_df[['down_time_reason', 'down_time_qty']].groupby(['down_time_reason']).sum()
      down_time_agg_dict = down_time_agg.to_dict()['down_time_qty']

      # Calculate downtime aggregations for day shift
      defects_agg = day_shift_df[['defects', 'defects_qty']].groupby(['defects']).sum()
      defects_agg_dict = defects_agg.to_dict()['defects_qty']

      return {
        "date": self.current_date.isoformat(),
        "hours": self.shift_hours,
        "downtime": down_time_agg_dict,
        "downtime_colors": generate_hex_colors(len(down_time_agg_dict)),
        "defects": defects_agg_dict,
        "defect_colors": generate_hex_colors(len(defects_agg_dict)),
        "rates": day_rates_table,
        "goals": day_goals_table,
        "reality": day_reality_table,
        "data": day_shift_table,
      }

  def __str__(self):
    shift_hours = ", ".join(self.shift_hours)
    has_conn = True if self.conn else False
    return f"DayShift date={self.current_date.isoformat()} shift_hours=[{shift_hours}] conn={has_conn} query=[{self.query}]"

def get_query_df(query):
  return pd.read_sql_query(
      sql= query,
      con=engine)

def get_daily_shift_data(shift_date):
  day_shift_query= current_app.session.query(models.Contact).filter_by(shift_date=shift_date).statement
  day_shift =  DayShift(shift_date, SHIFT_HOURS, query=day_shift_query, conn=engine)
  return day_shift.get_day_shift_table()
  
