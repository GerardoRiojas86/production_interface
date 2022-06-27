
from textwrap import indent
from dotenv import load_dotenv
load_dotenv()

import json
import datetime
import pandas as pd 
import werkzeug
from flask import Flask, _app_ctx_stack, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from sqlalchemy.orm import scoped_session

from . import models
from .database import SessionLocal, engine
from .contact_repository import get_daily_shift_data

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)

CORS(app)
                                                     
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack)

#settings
app.secret_key = 'mysecretkey'

@app.route('/')
def index():

    shift_date = datetime.datetime.today().strftime('%Y-%m-%d')
    # shift_date_data = app.session.query(models.Contact).filter_by(shift_date=shift_date).order_by(models.Contact.shift_hours.asc()).all()
    # shift_data_query= app.session.query(models.Contact).filter_by(shift_date=shift_date).order_by(models.Contact.shift_hours.asc()).statement
    
    shift_date_data = get_daily_shift_data(shift_date)

    print(json.dumps(shift_date_data, indent=4))

    # shift_data_df = pd.read_sql_query(
    #   sql= shift_data_query,
    #   con=engine)

    # down_time_group_sum = shift_data_df.groupby('down_time_reason').sum()
    # down_time_sum_labels = [val for val in down_time_group_sum.index.values]
    # down_time_sum_qty = down_time_group_sum['down_time_qty'].tolist()

    # print(list(shift_date_data['data'].values()))
    return render_template('index.html', 
                            shift_date=shift_date, 
                            data=shift_date_data['data'], 
                            rate=list(shift_date_data['rates'].values()), 
                            goal=list(shift_date_data['goals'].values()), 
                            reality=list(shift_date_data['reality'].values()),
                            downtime_labels=list(shift_date_data['downtime'].keys()),
                            downtime_sum=list(shift_date_data['downtime'].values()),
                            downtime_colors=shift_date_data['downtime_colors'],
                            defect_labels=list(shift_date_data['defects'].keys()),
                            defect_sum=list(shift_date_data['defects'].values()),
                            defect_colors=shift_date_data['defect_colors'])

@app.route('/add_contact', methods=['POST'])
def add_contact():
    
    if request.method == 'POST':
        contact = models.Contact(
            shift_date=datetime.datetime.strptime(request.form['shift_date'],'%Y-%m-%d').date(),
            shift_hours=request.form['shift_hours'],
            model=request.form['model'],
            clip_machine=request.form['clip_machine'],
            goal=request.form['goal'],
            rate=request.form['rate'],
            reality=request.form['reality'],
            defects=request.form['defects'],
            defects_qty=request.form['defects_qty'],
            down_time_reason=request.form['down_time_reason'],
            down_time_qty=request.form['down_time_qty']
        )   

        app.session.add(contact)
        app.session.commit()
        flash('Contact Added successfully')
        return redirect(url_for('index'))

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    contact = app.session.query(models.Contact).filter_by(id=id).first()

    if request.method == 'GET':
      return render_template('edit-contact.html', contact = contact)

    elif request.method == 'POST':
        if request.form['shift_date']: contact.shift_date=datetime.datetime.strptime(request.form['shift_date'],'%Y-%m-%d').date()
        if request.form['shift_hours']: contact.shift_hours=request.form['shift_hours']
        if request.form['model']: contact.model=request.form['model']
        if request.form['clip_machine']: contact.clip_machine=request.form['clip_machine']
        if request.form['goal']: contact.goal=request.form['goal']
        if request.form['rate']: contact.rate=request.form['rate']
        if request.form['reality']: contact.reality=request.form['reality']
        if request.form['defects']: contact.defects=request.form['defects']
        if request.form['defects_qty']: contact.defects_qty=request.form['defects_qty']
        if request.form['down_time_reason']: contact.down_time_reason=request.form['down_time_reason']
        if request.form['down_time_qty']: contact.down_time_qty=request.form['down_time_qty']

        app.session.add(contact)
        app.session.commit()

        flash('Contact Updated Successfully')
        return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    contact = app.session.query(models.Contact).filter_by(id=id).first()
    app.session.delete(contact)
    app.session.commit()

    flash('Contact Removed Successfully')
    return redirect(url_for('index'))

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    print(f'handling a bad request: {e}')
    return 'bad request!', 400

@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_bad_request(e):
    print('handling 500 error')
    return 'bad request!', 500