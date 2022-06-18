from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Desarrollo1169'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

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
        Plan = request.form['Plan']
        production = request.form['production']
        down_time = request.form['down_time']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (Plan, production, down_time) VALUES (%s, %s, %s)', (Plan, production, down_time))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = {0}'.format(id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        Plan = request.form['Plan']
        production = request.form['production']
        down_time = request.form['down_time']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET Plan = %s,
                down_time = %s,
                production = %s
            WHERE id = %s
        """, (Plan, down_time, production, id))
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

if __name__ == '__main__':
    app.run(port = 80, debug = True)