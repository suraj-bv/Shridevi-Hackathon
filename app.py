# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import config

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Config
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

# Routes
@app.route('/')
def index():
    return render_template('login_signup.html')

@app.route('/register', methods=['POST'])
def register():
    if request.form.get('role') == 'farmer':
        username = request.form['username']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO farmers (username, phone, email, password) VALUES (%s, %s, %s, %s)", 
                        (username, phone, email, hashed_password))
            mysql.connection.commit()
            cur.close()
            flash('Registration successful! Please log in.', 'success')
        except Exception as e:
            flash('Registration failed. Please try again.', 'danger')
    else:
        flash('Only farmers can register here.', 'warning')
    
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    role = request.form.get('role')
    
    cur = mysql.connection.cursor()
    user = None
    password_index = None

    try:
        if role == 'farmer':
            cur.execute("SELECT * FROM farmers WHERE username=%s", (username,))
            user = cur.fetchone()
            password_index = 4  # Password is at index 4 for farmers
        elif role == 'admin':
            cur.execute("SELECT * FROM admins WHERE username=%s", (username,))
            user = cur.fetchone()
            password_index = 2  # Password is at index 2 for admins
    except Exception as e:
        flash('An error occurred while trying to log in. Please try again.', 'danger')
        return redirect(url_for('index'))
    finally:
        cur.close()
    
    # if user and check_password_hash(user[password_index], password):
    #     # Store user role and name in session for page navigation
    #     session['username'] = username
    #     session['role'] = role

    #     # Redirect to role-specific homepage
    #     if role == 'farmer':
    #         return render_template('farmer_homepage.html', username=username)
    #     elif role == 'admin':
    #         return render_template('admin_homepage.html', username=username)
    # else:
    #     flash('Invalid credentials, please try again.', 'danger')
    #     return redirect(url_for('index'))


    if role == 'farmer':
        if user and check_password_hash(user[password_index], password):
            session['username'] = username
            session['role'] = role
            return render_template('farmer_homepage.html', username=username)
        else:
            flash('Invalid credentials, please try again.', 'danger')
            return redirect(url_for('index'))
    if role == 'admin':
        if user and (user[password_index] and password):
            session['username'] = username
            session['role'] = role
            return render_template('admin_homepage.html', username=username)
        else:
            flash('Invalid credentials, please try again.', 'danger')
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
