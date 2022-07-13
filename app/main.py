
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
from .repositories.production import get_shift_data, production_exist

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)

CORS(app)
                                                     
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack)

#settings
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
  current_date = datetime.datetime.today().strftime('%Y-%m-%d')
  current_project = 'Clip machine'
  shift_data = get_shift_data(current_date, current_project)

  # print(json.dumps(shift_data, indent=4))

  return render_template('index.html', 
                          shift_date=current_date,
                          hours=shift_data['hours'],
                          colors=shift_data['colors'],
                          production=shift_data['production'],
                          downtimes=shift_data['downtimes'],
                          defects=shift_data['defects']
                        )

@app.route('/report')
def report():
  current_date = datetime.datetime.today().strftime('%Y-%m-%d')
  project = 'Clip machine'

  return render_template('input-shift-report.html', 
                          shift_date=current_date,
                          project=project)

@app.route('/data')
def data():

  current_date = datetime.datetime.today().strftime('%Y-%m-%d')
  current_project = 'Clip machine'
  shift_data = get_shift_data(current_date, current_project)
  
  current_date = datetime.datetime.today().strftime('%Y-%m-%d')
  project = 'Clip machine'

  return render_template('shift-data.html', 
                          shift_date=current_date,
                          project=project,
                          data=shift_data['data'])

@app.route('/production', methods = ['GET'])
def get_production():
    production = app.session.query(models.Production).all()
    production_dict = [item.to_dict() for item in production]

    if request.method == 'GET':
      return jsonify(production_dict)

@app.route('/add_production', methods=['POST'])
def add_production():
    
    if request.method == 'POST':

      shift_date = datetime.datetime.strptime(request.form['shift_date'],'%Y-%m-%d').date()

      if production_exist(shift_date, request.form['shift_time']):
        flash('Production report already exist!', 'error')
        return redirect(url_for('report'))
      
      else:
        production = models.Production(
          project=request.form['project'],
          shift_date=shift_date,
          shift_time=request.form['shift_time'],
          machine=request.form['machine'],
          model=request.form['model'],
          quantity=request.form['quantity']
        )   

        app.session.add(production)
        app.session.commit()
        flash('Production added successfully', 'success')
        return redirect(url_for('report'))

@app.route('/update_production/<id>', methods = ['PATCH'])
def update_production(id):
    production = app.session.query(models.Production).filter_by(id=id).first()

    if (request.method == 'PATCH' and production != None):

      if ('project' in request.form.keys()): production.project=request.form['project'] 
      if ('shift_date' in request.form.keys()): production.shift_date=datetime.datetime.strptime(request.form['shift_date'],'%Y-%m-%d').date()
      if ('shift_time' in request.form.keys()): production.shift_time=request.form['shift_time']
      if ('model' in request.form.keys()): production.model=request.form['model']
      if ('machine' in request.form.keys()): production.machine=request.form['machine']
      if ('quantity' in request.form.keys()): production.quantity=request.form['quantity']

      app.session.add(production)
      app.session.commit()

      flash('Production updated Successfully')
      return redirect(url_for('index'))
    else:
      flash('Unknown production ID')
      return redirect(url_for('index'))

@app.route('/delete_production/<string:id>', methods= ['DELETE'])
def delete_production(id):
    production = app.session.query(models.Production).filter_by(id=id).first()
    app.session.delete(production)
    app.session.commit()

    flash('Production removed Successfully')
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
      flash('Defect added successfully', 'success')
      return redirect(url_for('report'))

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

@app.route('/delete_defect/<string:id>', methods= ['DELETE'])
def delete_defect(id):
    defect = app.session.query(models.Defect).filter_by(id=id).first()
    app.session.delete(defect)
    app.session.commit()

    flash('Defect removed Successfully')
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
        flash('Downtime added successfully', 'success')
        return redirect(url_for('report'))

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

@app.route('/delete_downtime/<string:id>', methods= ['DELETE'])
def delete_downtime(id):
    downtime = app.session.query(models.DownTime).filter_by(id=id).first()
    app.session.delete(downtime)
    app.session.commit()

    flash('Downtime removed Successfully')
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