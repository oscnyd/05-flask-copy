from flask import Flask, render_template, url_for, request
import sqlite3 as sql

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for the login page
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        try:
            # Get user input from the form
            user = request.form['user']
            pwd = request.form['pwd']

            # Connect to the database
            with sql.connect("database.db") as con:
                cur = con.cursor()
                try:
                    # Query to check if the user exists
                    sqlite_select_query = """SELECT * FROM LoginInformasjon WHERE user = '""" + user + """' AND pwd = '""" + pwd + """'"""
                    cur.execute(sqlite_select_query)
                    records = cur.fetchall()
                    if len(records) >= 1:
                        msg = "Login successful"
                    else:
                        msg = "Login failed"
                except:
                    msg = "Login failed"
        except:
            msg = "error in insert operation" + " " + msg
        finally:
            # Render the result page with the message
            return render_template("result.html", msg=msg)
            con.close()

# Route to display the form for adding a new student
@app.route('/enternew')
def new_student():
    return render_template('student.html')

# Route to add a new user to the database
@app.route('/addrec', methods=['POST','GET'])
def addrec():
    if request.method == 'POST':
        try:
            # Get user input from the form
            user = request.form['user']
            pwd = request.form['pwd']

            # Connect to the database
            with sql.connect("database.db") as con:
                cur = con.cursor()
                # Insert the new user into the database
                cur.execute("INSERT INTO LoginInformasjon (user, pwd) VALUES (?,?)",(user, pwd))
                con.commit()
                msg = "User successfully added"
        except:
            con.rollback()
            msg="error in insert operation"
        finally:
            # Render the result page with the message
            return render_template("result.html", msg=msg)
            con.close()

# Route to list all users
@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    # Query to select all users
    cur.execute("select * from LoginInformasjon")
    rows = cur.fetchall()
    # Render the list page with the users
    return render_template('list.html',rows=rows)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
