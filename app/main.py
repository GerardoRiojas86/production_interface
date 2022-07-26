
from dotenv import load_dotenv
load_dotenv()

import datetime
import werkzeug
from flask import Flask, _app_ctx_stack, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from sqlalchemy.orm import scoped_session

from . import models
from .database import SessionLocal, engine
from .repositories.production import get_shift_data, production_exist
from .repositories.project import add_project_machine, add_project_reason, get_project_by_id, get_projects, add_project, add_project_model


try:

  models.Base.metadata.create_all(bind=engine, checkfirst=True)

except Exception as e:
  print("Error occurred while DB setup: ", e)

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

CORS(app)
                                                     
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack)

#settings
app.secret_key = 'mysecretkey'

@app.route('/', methods=['GET'])
def home():
  data = get_projects()
  print(data)
  return render_template('projects.html', projects=data, add_project=True)

@app.route('/projects/form', methods=['GET'])
def show_project_form():
  projects = get_projects()

  return render_template('add-project.html', projects=projects)

@app.route('/project/add', methods=['POST'])
def submit_project():

  if request.method == 'POST':

    project = add_project(
      name=request.form['project_name'], 
      rate=request.form['project_rate'],
      goal=request.form['project_goal']
    )

    if project:
      flash('Project added successfully', 'success')
      return redirect(url_for('show_project_form'))
    
    else:
      flash('Unable to create project', 'error')
      return redirect(url_for('show_project_form'))

@app.route('/project/add/model', methods=['POST'])
def submit_project_model():

  if request.method == 'POST':

    model = add_project_model(
      name=request.form['model_name'], 
      project_id=request.form['project_id']
    )

    if model:
      flash('Project model added successfully', 'success')
      return redirect(url_for('show_project_form'))
    
    else:
      flash('Unable to create project model', 'error')
      return redirect(url_for('show_project_form'))

@app.route('/project/add/machine', methods=['POST'])
def submit_project_machine():

  if request.method == 'POST':

    model = add_project_machine(
      name=request.form['machine_name'], 
      project_id=request.form['project_id']
    )

    if model:
      flash('Project machine added successfully', 'success')
      return redirect(url_for('show_project_form'))
    
    else:
      flash('Unable to create project machine', 'error')
      return redirect(url_for('show_project_form'))

@app.route('/project/add/reason', methods=['POST'])
def submit_project_reason():

  if request.method == 'POST':

    model = add_project_reason(
      category=request.form['category'], 
      project_id=request.form['project_id'],
      description=request.form['description']
    )

    if model:
      flash('Project reason added successfully', 'success')
      return redirect(url_for('show_project_form'))
    
    else:
      flash('Unable to create project reason', 'error')
      return redirect(url_for('show_project_form'))

@app.route('/project/<id>', methods=['GET', 'POST'])
def show_project(id):
  
  project = get_project_by_id(id)

  if request.method == 'POST':
    if request.form['shift_date']:
      current_date = request.form['shift_date'] 
    else:
      current_date = datetime.datetime.today().strftime('%Y-%m-%d')
    
  elif request.method == 'GET':
    current_date = datetime.datetime.today().strftime('%Y-%m-%d')

  shift_data = get_shift_data(current_date, project['id'], project['rate'], project['goal'])

  return render_template('project.html', 
                          project=project,
                          shift_date=current_date,
                          hours=shift_data['hours'],
                          colors=shift_data['colors'],
                          production=shift_data['production'],
                          downtimes=shift_data['downtimes'],
                          defects=shift_data['defects']
                        )

@app.route('/project/<id>/report', methods=['GET'])
def report(id):

  project = get_project_by_id(id)
  current_date = datetime.datetime.today().strftime('%Y-%m-%d')
  

  return render_template('input-shift-report.html', 
                          shift_date=current_date,
                          project=project)

@app.route('/data', methods=['GET', 'POST'])
def data():

  if request.method == 'POST': 
    shift_date= request.form['shift_date']
  
  elif request.method == 'GET': 
    shift_date = datetime.datetime.today().strftime('%Y-%m-%d')

  project_id = 1
  shift_data = get_shift_data(shift_date, project_id)

  return render_template('shift-data.html', 
                          shift_date=shift_date,
                          project_id=project_id,
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

      if production_exist(shift_date, request.form['shift_time'], request.form['project_id']):
        flash('Production report already exist!', 'error')
        return redirect(url_for('report', id=request.form['project_id']))
      
      else:
        production = models.Production(
          project_id=request.form['project_id'],
          shift_date=shift_date,
          shift_time=request.form['shift_time'],
          machine=request.form['machine'],
          model=request.form['model'],
          quantity=request.form['quantity']
        )   

        app.session.add(production)
        app.session.commit()
        flash('Production added successfully', 'success')
        return redirect(url_for('report', id=request.form['project_id']))

@app.route('/update_production/<id>', methods = ['PATCH'])
def update_production(id):
    production = app.session.query(models.Production).filter_by(id=id).first()

    if (request.method == 'PATCH' and production != None):

      if ('project_id' in request.form.keys()): production.project_id=request.form['project_id'] 
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

@app.route('/defects', methods = ['GET'])
def get_defects():
    defect = app.session.query(models.Defect).all()
    defect_dict = [item.to_dict() for item in defect]

    if request.method == 'GET':
      return jsonify(defect_dict)

@app.route('/add_defect', methods=['POST'])
def add_defect():
    
    if request.method == 'POST':
      defect = models.Defect(
        project_id=request.form['project_id'],
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
      return redirect(url_for('report', id=request.form['project_id']))

@app.route('/update_defect/<id>', methods = ['PATCH'])
def update_defect(id):
    defect = app.session.query(models.Defect).filter_by(id=id).first()

    if (request.method == 'PATCH' and defect != None):

      if ('project_id' in request.form.keys()): defect.project_id=request.form['project_id'] 
      if ('shift_date' in request.form.keys()): defect.shift_date=datetime.datetime.strptime(request.form['shift_date'],'%Y-%m-%d').date()
      if ('shift_time' in request.form.keys()): defect.shift_time=request.form['shift_time']
      if ('model' in request.form.keys()): defect.model=request.form['model']
      if ('machine' in request.form.keys()): defect.machine=request.form['machine']
      if ('reason' in request.form.keys()): defect.reason=request.form['reason']
      if ('quantity' in request.form.keys()): defect.quantity=request.form['quantity']

      app.session.add(defect)
      app.session.commit()

      flash('Defect updated Successfully')
      return redirect(url_for('report', id=request.form['project_id']))
    else:
      flash('Unknown defect ID')
      return redirect(url_for('index'))

@app.route('/delete_defect/<string:id>', methods= ['DELETE'])
def delete_defect(id):
    defect = app.session.query(models.Defect).filter_by(id=id).first()
    app.session.delete(defect)
    app.session.commit()

    flash('Defect removed Successfully')
    return redirect(url_for('report', id=request.form['project_id']))

@app.route('/downtimes', methods = ['GET'])
def get_downtime():
    downtime = app.session.query(models.DownTime).all()
    downtime_dict = [item.to_dict() for item in downtime]

    if request.method == 'GET':
      return jsonify(downtime_dict)

@app.route('/add_downtime', methods=['POST'])
def add_downtime():
    
    if request.method == 'POST':
        downtime = models.DownTime(
          project_id=request.form['project_id'],
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
        return redirect(url_for('report', id=request.form['project_id']))

@app.route('/update_downtime/<id>', methods = ['PATCH'])
def update_downtime(id):
    downtime = app.session.query(models.DownTime).filter_by(id=id).first()

    if (request.method == 'PATCH' and downtime != None):
      if ('project_id' in request.form.keys()): downtime.project_id=request.form['project_id'] 
      if ('shift_date' in request.form.keys()): downtime.shift_date=datetime.datetime.strptime(request.form['shift_date'],'%Y-%m-%d').date()
      if ('shift_time' in request.form.keys()): downtime.shift_time=request.form['shift_time']
      if ('model' in request.form.keys()): downtime.model=request.form['model']
      if ('machine' in request.form.keys()): downtime.machine=request.form['machine']
      if ('reason' in request.form.keys()): downtime.reason=request.form['reason']
      if ('quantity' in request.form.keys()): downtime.quantity=request.form['quantity']

      app.session.add(downtime)
      app.session.commit()

      flash('Downtime updated Successfully')
      return redirect(url_for('index', id=request.form['project_id']))
    else:
      flash('Unknown downtime ID')
      return redirect(url_for('report', id=request.form['project_id']))

@app.route('/delete_downtime/<string:id>', methods= ['DELETE'])
def delete_downtime(id):
    downtime = app.session.query(models.DownTime).filter_by(id=id).first()
    app.session.delete(downtime)
    app.session.commit()

    flash('Downtime removed Successfully')
    return redirect(url_for('report', id=request.form['project_id']))

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400

@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_bad_request(e):
    return 'bad request!', 500

@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_not_found(e):
  return render_template('not_found.html')