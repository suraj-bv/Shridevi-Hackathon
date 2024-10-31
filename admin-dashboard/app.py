from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database connection function
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",         # Replace with your MySQL username
        password="Prem@123", # Replace with your MySQL password
        database="admin_dashboard"
    )
    return conn

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('main_page.html')

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
