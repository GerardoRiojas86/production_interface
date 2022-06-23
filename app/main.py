
from dotenv import load_dotenv
load_dotenv()

import datetime

import werkzeug
from flask import Flask, _app_ctx_stack, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from sqlalchemy.orm import scoped_session

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
CORS(app)
                                                     
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack)

#settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    contacts = app.session.query(models.Contact).all()
    return render_template('index.html', contacts = contacts)

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
        return redirect(url_for('Index'))

@app.route('/report', methods=['GET', 'POST'])
def get_report():  

    if request.method == 'GET':  
        shift_date = datetime.datetime.today().strftime('%Y-%m-%d')
        shift_date_data = app.session.query(models.Contact).filter_by(shift_date=shift_date).all()
        rate = [row.rate for row in shift_date_data]
        goal = [row.goal for row in shift_date_data]
        reality = [row.reality for row in shift_date_data]
        
        return render_template('report.html', shift_date=shift_date, daily_rate=rate, daily_goal=goal, daily_reality=reality)
    
    if request.method == 'POST':
        shift_date = request.form['shift_date']
        shift_date_data = app.session.query(models.Contact).filter_by(shift_date=shift_date).all()
        rate = [row.rate for row in shift_date_data]
        goal = [row.goal for row in shift_date_data]
        reality = [row.reality for row in shift_date_data]
        
        return render_template('report.html', shift_date=shift_date, daily_rate=rate, daily_goal=goal, daily_reality=reality)
    
    #return redirect(url_for('book_list.html'))

@app.route('/edit/<id>')
def get_contact(id):
    contact = app.session.query(models.Contact).filter_by(id=id).first()
    return render_template('edit-contact.html', contact = contact)

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    contact = app.session.query(models.Contact).filter_by(id=id).first()

    print(f'Updating contact ID: {contact.id}')

    if request.method == 'POST':

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
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    contact = app.session.query(models.Contact).filter_by(id=id).first()
    app.session.delete(contact)
    app.session.commit()

    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

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