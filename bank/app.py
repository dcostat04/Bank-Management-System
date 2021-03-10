import pymysql
from flask import Flask, flash,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

import time
import datetime
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'TIGER'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'trevor@0409'
app.config['MYSQL_DB'] = 'bank'

mysql = MySQL(app)
ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT id,name,email,balance FROM users" )

	data1 = cursor.fetchall()


	return render_template('index.html',data=data1)

@app.route('/transaction',methods=['GET', 'POST'])
def make():
	msg = 'Please enter details to be added'
	if request.method == 'POST' and 'sender' in request.form and 'receiver' in request.form and 'email' in request.form and 'amount' in request.form:
		sender = request.form['sender']
		receiver = request.form['receiver']
		email = request.form['email']
		amount = request.form['amount']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("INSERT INTO transaction (sender, receiver,email, int(amount)) VALUES ( %s, %s, %s,%s)", (sender, receiver,email, int(amount)))
		mysql.connection.commit()
		cursor.close()
		msg = 'You have successfully transacted!'
	elif request.method == 'POST':
		msg = 'Please fill out the form!'
	return render_template('make.html',msg=msg)

@app.route('/history')
def transhis():
	cursor = mysql.connection.cursor()
	cursor.execute('SELECT * FROM transaction ORDER BY sno,`datetime` DESC')
	data1 = cursor.fetchall()
	cursor.execute('SELECT * FROM transaction GROUP BY date(`datetime`)')
	data2 = cursor.fetchall()
	return render_template('tranhis.html', data=data1, data2=data2)

if __name__=="__main__":
    app.run(debug=True);