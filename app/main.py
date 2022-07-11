
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
    return 'OK'

    # shift_date = datetime.datetime.today().strftime('%Y-%m-%d')
    
    # shift_date_data = get_daily_shift_data(shift_date)

    # print(json.dumps(shift_date_data, indent=4))


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

@app.route('/production', methods = ['GET'])
def get_production():
    production = app.session.query(models.Production).all()
    production_dict = [item.to_dict() for item in production]

    if request.method == 'GET':
      return jsonify(production_dict)

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

@app.route('/update_production/<id>', methods = ['PATCH'])
def update_production(id):
    production = app.session.query(models.Production).filter_by(id=id).first()

    if (request.method == 'PATCH' and production != None):

      if ('project' in request.form.keys()): production.project=request.form['project'] 
      if ('shift_date' in request.form.keys()): production.shift_date=datetime.datetime.strptime(request.form['shift_date'],'%Y-%m-%d').date()
      if ('shift_time' in request.form.keys()): production.shift_time=request.form['shift_time']
      if ('model' in request.form.keys()): production.model=request.form['model']
      if ('machine' in request.form.keys()): production.machine=request.form['machine']
      if ('goal' in request.form.keys()): production.goal=request.form['goal']
      if ('rate' in request.form.keys()): production.rate=request.form['rate']
      if ('quantity' in request.form.keys()): production.quantity=request.form['quantity']

      app.session.add(production)
      app.session.commit()

      flash('Production updated Successfully')
      return redirect(url_for('index'))
    else:
      flash('Unknown production ID')
      return redirect(url_for('index'))

@app.route('/defect', methods = ['GET'])
def get_defects():
    defect = app.session.query(models.Defect).all()
    defect_dict = [item.to_dict() for item in defect]

    if request.method == 'GET':
      return jsonify(defect_dict)

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

@app.route('/update_defect/<id>', methods = ['PATCH'])
def update_defect(id):
    defect = app.session.query(models.Defect).filter_by(id=id).first()

    if (request.method == 'PATCH' and defect != None):

      if ('project' in request.form.keys()): defect.project=request.form['project'] 
      if ('shift_date' in request.form.keys()): defect.shift_date=datetime.datetime.strptime(request.form['shift_date'],'%Y-%m-%d').date()
      if ('shift_time' in request.form.keys()): defect.shift_time=request.form['shift_time']
      if ('model' in request.form.keys()): defect.model=request.form['model']
      if ('machine' in request.form.keys()): defect.machine=request.form['machine']
      if ('reason' in request.form.keys()): defect.reason=request.form['reason']
      if ('quantity' in request.form.keys()): defect.quantity=request.form['quantity']

      app.session.add(defect)
      app.session.commit()

      flash('Defect updated Successfully')
      return redirect(url_for('index'))
    else:
      flash('Unknown defect ID')
      return redirect(url_for('index'))

@app.route('/downtime', methods = ['GET'])
def get_downtime():
    downtime = app.session.query(models.DownTime).all()
    downtime_dict = [item.to_dict() for item in downtime]

    if request.method == 'GET':
      return jsonify(downtime_dict)

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

@app.route('/update_downtime/<id>', methods = ['PATCH'])
def update_downtime(id):
    downtime = app.session.query(models.DownTime).filter_by(id=id).first()

    if (request.method == 'PATCH' and downtime != None):
      if ('project' in request.form.keys()): downtime.project=request.form['project'] 
      if ('shift_date' in request.form.keys()): downtime.shift_date=datetime.datetime.strptime(request.form['shift_date'],'%Y-%m-%d').date()
      if ('shift_time' in request.form.keys()): downtime.shift_time=request.form['shift_time']
      if ('model' in request.form.keys()): downtime.model=request.form['model']
      if ('machine' in request.form.keys()): downtime.machine=request.form['machine']
      if ('reason' in request.form.keys()): downtime.reason=request.form['reason']
      if ('quantity' in request.form.keys()): downtime.quantity=request.form['quantity']

      app.session.add(downtime)
      app.session.commit()

      flash('Downtime updated Successfully')
      return redirect(url_for('index'))
    else:
      flash('Unknown downtime ID')
      return redirect(url_for('index'))

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400

@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_bad_request(e):
    return 'bad request!', 500