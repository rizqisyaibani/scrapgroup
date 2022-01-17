from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_mysqldb import MySQL
from werkzeug.exceptions import abort
from bs4 import BeautifulSoup


from web_scrap import scrape_func
import requests
import MySQLdb.cursors
import mysql.connector
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'scrape'

mysql = MySQL(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg='')

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))


@app.route('/admin')
def admin():
    if request.method == 'POST':
        title = request.form['title']

        if not title:
            flash('Title is required!')
        else:
            mydb = get_db_connection()
            cursor = mydb.cursor()
            cursor.execute('INSERT INTO posts (title, content) VALUES (%s, %s)',
                         (title, content))
            mydb.commit()
            mydb.close()
            return redirect(url_for('home'))
        
    return render_template('admin.html')

@app.route('/admin/scrape', methods=('GET', 'POST'))
def scrape():
    if request.method == 'POST':
        link = request.form['link']
        result = scrape_func(link)

        if not link:
            flash('Where is your url?')
        else:
            mydb = mysql.connection
            cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO books (cover, title, descr, author, publisher, pub_date, genres, lang, pages, comp, price, rating, tot_rat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (result['cover'], result['title'], result['descr'], result['author'], result['publisher'], result['pub_date'], result['genres'], result['lang'], result['pages'], result['comp'], result['price'], result['rat'], result['tot_rat']))
            mydb.commit()
            mydb.close()
            return redirect(url_for('report'))
        return 'Where is your url?'
        
    return render_template('scrape.html')
    
    
@app.route('/admin/scrape/report', methods=('GET', 'POST'))
def report():
    return render_template('scrape_report.html')


@app.route('/admin/bookmenu', methods=('POST',))
def bookmenu():
    return render_template('book_menu.html')

@app.route('/admin/dashboard', methods=('POST',))
def dashboard():
    return render_template('dashboard.html')
