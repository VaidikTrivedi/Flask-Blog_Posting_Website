from flask import Flask, render_template, flash, redirect, request, url_for, session, logging
#from data import Articles
from flask_mysqldb import MySQL
import MySQLdb
from wtforms import StringField, PasswordField, validators, TextAreaField, Form
from passlib.hash import sha256_crypt
from functools import wraps
from flask_ckeditor import CKEditor

app = Flask(__name__)

#Config mySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'FlaskApp'
app.config['MYSQL_PORT'] = 3305
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['CKEDITOR_PKG_TYPE'] = 'basic'

#init MYSQL
mysql = MySQL(app)
print("MySQL: ", mysql)

#init CKEditor
ckeditor = CKEditor(app)

#Articles = Articles()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()

    if result>0:
        return render_template('articles.html', articles = articles)
    else:
        flash("No Articles Found!")
        return render_template('articles.html')
    cur.close()

@app.route('/article/<string:id>/')
def article(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()

    if result>0:
        return render_template('article.html', article = article)
    else:
        flash('No Data Found! Please Try Again.')
        return render_template('article.html')
    cur.close()

#Register Form
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(), 
        validators.EqualTo('confirm', message='Password does not match')
        ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if(request.method=='POST' and form.validate()):
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #Create Cursor
        cur = mysql.connection.cursor()
        # conn = MySQLdb.connect(host="127.0.0.1", port=3305, user="root", password="", db="FlaskApp")
        # Cur = conn.cursor()
        print("\n\n\nCursor: ", cur)

        cur.execute("INSERT INTO users (name, email, username, password, role) VALUES  (%s, %s, %s, %s, %s)", (name, email, username, password, 'writer'))

        #Commit to DB
        mysql.connection.commit()

        cur.close()

        flash('You are now registered can able to login', 'success')

        return redirect(url_for('index'))
        
    return render_template('register.html', form=form)

#User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        role = request.form['role']

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM users WHERE username = %s AND role = %s", ([username], role))

        if result > 0:
            data = cur.fetchone()
            print("\n\nData: ", data, "\n\n")
            password = data['password']

            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                session['role'] = role

                flash("You are now logged in", 'success')
                return redirect(url_for('dashboard'))
            
            else:
                error = "Invalid Login"
                return render_template('login.html', error=error)
            
            cur.close()

        else:
            error = "Username or Password does not match for selected role"
            return render_template('login.html', error=error)

    return render_template('login.html')

#Check is user is logged in or not
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login first!', 'danger')
            return redirect(url_for('login'))
    return wrap

#Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash("You are successfully logged out", 'success')
    return redirect(url_for('login'))

#Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()
    if session['role'] == 'admin':
        result = cur.execute("SELECT * FROM articles")
    else:
        result = cur.execute("SELECT * FROM articles WHERE author = %s", [session['username']])

    articles = cur.fetchall()
    
    if result>0:
        return render_template('dashboard.html', articles=articles)
    else:
        #msg = "No Atticles Found!"
        return render_template('dashboard.html')
    
    cur.close()

#Article Form
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=20)])

#Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO articles(title, body, author) values (%s, %s, %s) ", (title, body, session['username']))
        mysql.connection.commit()
        cur.close()

        flash('Article Created', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_article.html', form=form)

@app.route('/edit_article/<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_article(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    print(result)
    article = cur.fetchone()
    cur.close()

    form = ArticleForm(request.form)

    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        cur = mysql.connection.cursor()
        #app.logger.info(title)
        cur.execute ("UPDATE articles SET title=%s, body=%s WHERE id=%s",(title, body, id))
        mysql.connection.commit()
        cur.close()
        flash('Article Updated Successfully', 'success')

        return redirect(url_for('dashboard'))
    return render_template('edit_article.html', form=form)


@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM articles WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Article Suceessfully Removed', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)