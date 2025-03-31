from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
CORS(app)  # Allows requests from frontend
DB_FILE = "students.sqlite" # Database file name

# Function for connecting to database
def openConnection(_dbFile):
    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("successfully opened connection")
    except Error as e:
        print(e)

    return conn

# Function for closing database connection
def closeConnection(_conn, _dbFile):
    print("Close database: ", _dbFile)
    try:
        _conn.close()
        print("successfully closed connection")
    except Error as e:
        print(e)

# == API CALL: ==
# GET/grades
# Input: None 
# Return: JSON of students with grades
@app.route('/grades', methods = ['GET'])
def returnAllStudents():
    conn = openConnection(DB_FILE)
    
    with conn:
        cursor = conn.cursor()
        
        # Get all contents from students table, store in data
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()
        
    closeConnection(conn, DB_FILE)
    
    # Return data as JSON
    return jsonify(dict(data))

# == API CALL: ==
# GET /grades/<student name>
# Input: None 
# Return: JSON of student with grades
@app.route('/grades/<string:name>', methods = ['GET'])
def returnStudent(name):
    conn = openConnection(DB_FILE)

    with conn:
        cursor = conn.cursor()
        
        # Get all contents from students where name matches, store in data
        cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        data = cursor.fetchall()
        
    closeConnection(conn, DB_FILE)

    # Return data as JSON
    return jsonify(dict(data))

# == API CALL: ==     
# POST /grades 
# Input: JSON of student name and corresponding grade, e.g. {"name": "John Doe", "grade": 92.1} 
# Return: JSON of student with grades after operation takes place
@app.route('/grades', methods = ['POST'])
def createStudent():
    conn = openConnection(DB_FILE)

    # Get JSON data from request
    requestData = request.get_json()

    with conn:
        cursor = conn.cursor()
        
        # Insert into students table new student tuple containing info from frontend
        cursor.execute("INSERT INTO students (name, grade) VALUES (?, ?)", (requestData["name"], requestData["grade"],))
        conn.commit()
        
        # Get all contents from students table, store in data
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()
        
    closeConnection(conn, DB_FILE)

    # Return data as JSON
    return jsonify(dict(data))

# == API CALL ==
# PUT /grades/<student name> 
# Input: JSON of the grade that corresponds to the student name in the URI, e.g. {"grade": 92.1} 
# Return: JSON of student with grades after operation takes place
@app.route('/grades/<string:name>', methods = ['PUT'])
def updateStudent(name):
    conn = openConnection(DB_FILE)

    # Get JSON data from request
    requestData = request.get_json()

    with conn:
        cursor = conn.cursor()
        
        # Change grade info where names match
        cursor.execute("UPDATE students SET grade = ? WHERE name = ?", (requestData["grade"], name,))
        conn.commit()
        
        # Get all contents from students table
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()
        
    closeConnection(conn, DB_FILE)

    # Return data as JSON
    return jsonify(dict(data))

# == API CALL ==
# DELETE /grades/<student name> 
# Input: None 
# Return: JSON of student with grades after operation takes place 
@app.route('/grades/<string:name>', methods = ['DELETE'])
def deleteStudent(name):
    conn = openConnection(DB_FILE)
    
    with conn:
        cursor = conn.cursor()
        
        # Delete from students table where name matches and commit changes to database
        cursor.execute("DELETE FROM students WHERE name = ?", (name,))
        conn.commit()
        
        # Fetch new student list
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()
        
    closeConnection(conn, DB_FILE)

    # Return data as JSON
    return jsonify(dict(data))
    
    
if __name__ == '__main__':
    app.run(debug=True)
    