from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_mysqldb import MySQL
from werkzeug.exceptions import abort
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

from bs4 import BeautifulSoup
from web_scrap import scrape_func

import requests
import MySQLdb.cursors
import mysql.connector
import re

import os
import pathlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'scrape'

app.secret_key = "scrapgroup.com"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "102269209906-qsk38k6jb0ij46iqu0a8f7efp4a61ok6.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

# def login_is_required(function):
#     def wrapper(*args, **kwargs):
#         if "google_id" not in session:
#             return abort(401)  # Authorization required
#         else:
#             return function()

#     return wrapper

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

@app.route('/googlelogin')
def googlelogin():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route("/callback")
def callback():
    # msg = ''
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    # return redirect("/protected_area")
    # return render_template('index.html', msg='')
    return redirect(url_for('protected_area'))


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
        mydb = mysql.connection
        cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM books')
        result = cursor.fetchall()
        for i in result:
            print(i)
            
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


@app.route('/book')
def book():
    return render_template('book.html')

@app.route('/book/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST' and 'link' in request.form:
        link = request.form['link']
        
        if link == '':
            flash('Where is your url?')
        else:
            result = scrape_func(link)
            mydb = mysql.connection
            cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO books (cover, title, descr, author, publisher, pub_date, genres, lang, pages, comp, price, rating, tot_rat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (result['cover'], result['title'], result['descr'], result['author'], result['publisher'], result['pub_date'], result['genres'], result['lang'], result['pages'], result['comp'], result['price'], result['rat'], result['tot_rat']))
            mydb.commit()
            mydb.close()
            return redirect(url_for('report'))
        
    return render_template('scrape.html')
    
    
@app.route('/book/scrape/report', methods=['GET', 'POST'])
def report():
    return render_template('scrape_report.html')


@app.route('/book/bookmenu', methods=['POST',])
def bookmenu():
    return render_template('book_menu.html')

@app.route('/book/dashboard', methods=['POST',])
def dashboard():
    return render_template('dashboard.html')

@app.route("/protected_area")
# @login_is_required
def protected_area():
    # if 'loggedin' in session:
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
    #     account = cursor.fetchone()
    #     return render_template('profile.html', account=account)
    # return redirect(url_for('home'))
    # return render_template('home.html', username=session['username'])
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)