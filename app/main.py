from dotenv import load_dotenv
load_dotenv()

import os

from flask import Flask, _app_ctx_stack, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from sqlalchemy.orm import scoped_session

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

template_dir = os.path.abspath('../production_interface/app/templates')

app = Flask(__name__, template_folder=template_dir)
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
            days=request.form['days'],
            model=request.form['model'],
            clip_machine=request.form['clip_machine'],
            hours=request.form['hours'],
            goal=request.form['goal'],
            rate=request.form['rate'],
            reality=request.form['reality'],
            defects=request.form['defects'],
            defects_qty=request.form['defects_qty'],
            down_time=request.form['down_time'],
            down_time_qty=request.form['down_time_qty']
        )

        app.session.add(contact)
        app.session.commit()

        flash('Contact Added successfully')
        return redirect(url_for('Index'))

@app.route('/report', methods=['GET'])
def get_report():    
    contacts = app.session.query(models.Contact).all()
    return render_template('book_list.html', contact=contacts)
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

        if request.form['days']: contact.days=request.form['days']
        if request.form['model']: contact.model=request.form['model']
        if request.form['clip_machine']: contact.clip_machine=request.form['clip_machine']
        if request.form['hours']: contact.hours=request.form['hours']
        if request.form['goal']: contact.goal=request.form['goal']
        if request.form['rate']: contact.rate=request.form['rate']
        if request.form['reality']: contact.reality=request.form['reality']
        if request.form['defects']: contact.defects=request.form['defects']
        if request.form['defects_qty']: contact.defects_qty=request.form['defects_qty']
        if request.form['down_time']: contact.down_time=request.form['down_time']
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
