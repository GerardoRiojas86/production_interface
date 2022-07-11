
from dotenv import load_dotenv
load_dotenv()

import json
import datetime
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

    # shift_date = datetime.datetime.today().strftime('%Y-%m-%d')
    
    # shift_date_data = get_daily_shift_data(shift_date)

    # print(json.dumps(shift_date_data, indent=4))

    return 'OK'
    # return render_template('index.html', 
    #                         shift_date=shift_date, 
    #                         data=shift_date_data['data'], 
    #                         rate=list(shift_date_data['rates'].values()), 
    #                         goal=list(shift_date_data['goals'].values()), 
    #                         reality=list(shift_date_data['reality'].values()),
    #                         downtime_labels=list(shift_date_data['downtime'].keys()),
    #                         downtime_sum=list(shift_date_data['downtime'].values()),
    #                         downtime_colors=shift_date_data['downtime_colors'],
    #                         defect_labels=list(shift_date_data['defects'].keys()),
    #                         defect_sum=list(shift_date_data['defects'].values()),
    #                         defect_colors=shift_date_data['defect_colors'])

@app.route('/add_production', methods=['POST'])
def add_production():
    
    if request.method == 'POST':
        production = models.Production(
          project=request.form['project'],
          shift_date=datetime.datetime.strptime(request.form['shift_date'],'%Y-%m-%d').date(),
          shift_time=request.form['shift_time'],
          machine=request.form['machine'],
          model=request.form['model'],
          goal=request.form['goal'],
          rate=request.form['rate'],
          quantity=request.form['quantity']
        )   

        app.session.add(production)
        app.session.commit()
        flash('Production added successfully')
        return redirect(url_for('index'))

@app.route('/add_defect', methods=['POST'])
def add_defect():
    
    if request.method == 'POST':
        defect = models.Defect(
          project=request.form['project'],
          shift_date=datetime.datetime.strptime(request.form['shift_date'],'%Y-%m-%d').date(),
          shift_time=request.form['shift_time'],
          machine=request.form['machine'],
          model=request.form['model'],
          reason=request.form['reason'],
          quantity=request.form['quantity']            
        )   

        app.session.add(defect)
        app.session.commit()
        flash('Defect added successfully')
        return redirect(url_for('index'))

@app.route('/add_downtime', methods=['POST'])
def add_downtime():
    
    if request.method == 'POST':
        downtime = models.DownTime(
          project=request.form['project'],
          shift_date=datetime.datetime.strptime(request.form['shift_date'],'%Y-%m-%d').date(),
          shift_time=request.form['shift_time'],
          machine=request.form['machine'],
          model=request.form['model'],
          reason=request.form['reason'],
          quantity=request.form['quantity']            
        )   

        app.session.add(downtime)
        app.session.commit()
        flash('Downtime added successfully')
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