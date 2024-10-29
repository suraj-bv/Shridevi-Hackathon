from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from flask_cors import CORS
import config

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)

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

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/register-problem', methods=['GET', 'POST'])
def register_problem():
    if request.method == 'POST':
        # Handle form submission
        name = request.form.get('name')
        contact = request.form.get('contact')
        crop = request.form.get('crop')
        issue = request.form.get('issue')
        additional_info = request.form.get('additionalInfo')

        # Insert data into MySQL
        try:
            cur = mysql.connection.cursor()
            query = """
                INSERT INTO problems1 (name, contact, crop, issue, additional_info)
                VALUES (%s, %s, %s, %s, %s)
            """
            cur.execute(query, (name, contact, crop, issue, additional_info))
            mysql.connection.commit()
            flash('Problem registered successfully!', 'success')
        except Exception as err:
            print(f"Error while inserting data: {err}")
            flash('Failed to register problem. Please try again.', 'error')
        finally:
            cur.close()

        return redirect(url_for('register_problem'))
    
    # Render problem registration form on GET request
    return render_template('prblm_reg.html')

@app.route('/farmer_dashboard')
def farmer_dashboard():
    if 'username' in session and session.get('role') == 'farmer':
        username = session['username']
        return render_template('farmer_dashboard.html', username=username)
    else:
        flash("Please log in to access the dashboard", "warning")
        return redirect(url_for('index'))






def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",         # Replace with your MySQL username
        password="mysql", # Replace with your MySQL password
        database="admin_dashboard"
    )
    return conn

# Route to serve the HTML page
# @app.route('/')
# def index():
#     return render_template('admin_homepage.html')

# Route to serve Card 1 page
@app.route('/index1')
def card1():
    return render_template('index1.html')  # Create this file in the templates folder

# Route to serve Card 2 page
@app.route('/index2')
def card2():
    return render_template('index2.html')  # Create this file in the templates folder

# Route to serve Card 3 page
@app.route('/index3')
def card3():
    return render_template('index3.html')  # Create this file in the templates folder

# Route to get all equipment records
@app.route('/api/equipment', methods=['GET'])
def get_equipment():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM equipment')
    equipment_records = cursor.fetchall()
    conn.close()
    return jsonify(equipment_records)

# Route to add a new equipment record
@app.route('/api/equipment', methods=['POST'])
def add_equipment():
    new_equipment = request.json
    name = new_equipment['name']
    type = new_equipment['type']
    quantity = new_equipment['quantity']
    price_per_day = new_equipment['price_per_day']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO equipment (name, type, quantity, price_per_day) VALUES (%s, %s, %s, %s)',
                   (name, type, quantity, price_per_day))
    conn.commit()
    conn.close()
    return jsonify(new_equipment), 201

# Route to delete an equipment record
@app.route('/api/equipment/<int:id>', methods=['DELETE'])
def delete_equipment(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM equipment WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return '', 204

# Route to get all labor records
@app.route('/api/labor', methods=['GET'])
def get_labor():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM labor')
    labor_records = cursor.fetchall()
    conn.close()
    return jsonify(labor_records)

# Route to add a new labor record
@app.route('/api/labor', methods=['POST'])
def add_labor():
    new_labor = request.json
    name = new_labor['name']
    age = new_labor['age']
    contact_no = new_labor['contact_no']
    address = new_labor['address']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO labor (name, age, contact_no, address) VALUES (%s, %s, %s, %s)',
                   (name, age, contact_no, address))
    conn.commit()
    conn.close()
    return jsonify(new_labor), 201

# Route to delete a labor record
@app.route('/api/labor/<int:id>', methods=['DELETE'])
def delete_labor(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM labor WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return '', 204

# Route to get all scheme records
@app.route('/api/schemes', methods=['GET'])
def get_schemes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM schemes')
    schemes_records = cursor.fetchall()
    conn.close()
    return jsonify(schemes_records)

# Route to add a new scheme record
@app.route('/api/schemes', methods=['POST'])
def add_scheme():
    new_scheme = request.json
    name = new_scheme['name']
    description = new_scheme['description']
    apply_link = new_scheme['apply_link']
    eligibility_criteria = new_scheme['eligibility_criteria']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO schemes (name, description, apply_link, eligibility_criteria) VALUES (%s, %s, %s, %s)',
                   (name, description, apply_link, eligibility_criteria))
    conn.commit()
    conn.close()
    return jsonify(new_scheme), 201

# Route to delete a scheme record
@app.route('/api/schemes/<int:id>', methods=['DELETE'])
def delete_scheme(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM schemes WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)