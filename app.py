from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_mysqldb import MySQL
from flask import _app_ctx_stack

from flask_cors import CORS

from sqlalchemy.orm import scoped_session

from . import models
from .database import SessionLocal, engine

app = Flask(__name__)

CORS(app)

app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
# Mysql Connection
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'flaskcontacts'
# mysql = MySQL(app)

#settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        days = request.form['days']
        model = request.form['model']
        clip_machine = request.form['clip_machine']
        hours = request.form['hours']
        goal = request.form['goal']
        rate = request.form['rate']
        reality = request.form['reality']
        defects = request.form['defects']
        defects_qty = request.form['defects_qty']
        down_time = request.form['down_time']
        down_time_qty = request.form['down_time_qty']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (days, model, clip_machine, hours, goal, rate, reality, defects, defects_qty, down_time, down_time_qty) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (days, model, clip_machine, hours, goal, rate, reality, defects, defects_qty, down_time, down_time_qty))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index'))

@app.route('/report', methods=['GET'])
def get_report():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts ')
    for tabla in cur:
        print(tabla)
    data = cur.fetchall()
    return render_template('book_list.html', contact = data)
    #return redirect(url_for('book_list.html'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = {0}'.format(id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        days = request.form['days']
        model = request.form['model']
        clip_machine = request.form['clip_machine']
        hours = request.form['hours']
        goal = request.form['goal']
        rate = request.form['rate']
        reality = request.form['reality']
        defects = request.form['defects']
        defects_qty = request.form['defects_qty']
        down_time = request.form['down_time']
        down_time_qty = request.form['down_time_qty']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET days = %s,
                clip_machine = %s,
                model = %s,
                hours = %s,
                goal = %s,
                rate = %s,
                reality = %s,
                defects = %s,
                defects_qty = %s,
                down_time = %s,
                down_time_qty = %s
            WHERE id = %s
        """, (days, clip_machine, model, hours, goal, rate, reality, defects, defects_qty, down_time, down_time_qty, id))
        mysql.connection.commit()
        flash('Contact Updated Successfully')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()
if __name__ == '__main__':
    app.run(port = 80, debug = True)