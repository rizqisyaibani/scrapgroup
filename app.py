from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="scrape"
    )

    return mydb

def get_post(post_id):
    mydb = get_db_connection()
    cursor = mydb.cursor()

    cursor.execute(
        'SELECT * FROM posts WHERE id = %s',
        (post_id,)
    )

    result = cursor.fetchone()
    post = {
        'id': result[0],
        'created': result[1],
        'title': result[2],
        'content': result[3]
    }
    mydb.close()

    if post is None:
        abort(404)
    return post


@app.route('/')
def index():
    mydb = get_db_connection()
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM book')
    result = cursor.fetchall()
    book = []
    for entry in result:
        record = {
            'cover': entry[0],
            'title': entry[1],
            'descr': entry[2],
            'author': entry[3],
            'publisher': entry[4],
            'pub_date': entry[5],
            'genres': entry[6],
            'lang': entry[7],
            'pages': entry[8],
            'comp': entry[9],
            'price': entry[10],
            'rating': entry[11],
            'tot_rat': entry[12]
        }
        book.append(record)
    mydb.close()
    
    return render_template('index.html')
    

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            mydb = get_db_connection()
            cursor = mydb.cursor()
            cursor.execute('INSERT INTO posts (title, content) VALUES (%s, %s)',
                         (title, content))
            mydb.commit()
            mydb.close()
            return redirect(url_for('index'))
        
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            mydb = get_db_connection()
            cursor = mydb.cursor()
            cursor.execute('UPDATE posts SET title = %s, content = %s'
                         ' WHERE id = %s',
                         (title, content, id))
            mydb.commit()
            mydb.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    mydb = get_db_connection()
    cursor = mydb.cursor()
    cursor.execute('DELETE FROM posts WHERE id = %s', (id,))
    mydb.commit()
    mydb.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

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
            return redirect(url_for('index'))
        
    return render_template('admin.html')

@app.route('/admin/scrape', methods=('GET', 'POST'))
def scrape():
    return render_template('scrape.html')

@app.route('/admin/scrape/report', methods=('POST',))
def report():
    return render_template('scrape_report.html')

@app.route('/admin/bookmenu', methods=('POST',))
def bookmenu():
    return render_template('book_menu.html')

@app.route('/admin/dashboard', methods=('POST',))
def dashboard():
    return render_template('dashboard.html')
