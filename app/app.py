from flask import Flask, render_template, request
from pymysql import connections
import os
import random
import argparse
import logging

app = Flask(__name__, static_url_path='/static')


DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "passwors"
DATABASE = os.environ.get("DATABASE") or "employees"
COLOR_FROM_ENV = os.environ.get('APP_COLOR') or "lime"
DBPORT = int(os.environ.get("DBPORT", "3306"))

# Background image downloaded through init container
BGIMG = "tmp/background.jpg"
# Background image URL to print
BGIMG_URL = os.environ.get("BGIMG_URL")
# Get name
OWN_NAME = os.environ.get("OWN_NAME")

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host= DBHOST,
    port=DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
)
output = {}
table = 'employee';

@app.route("/", methods=['GET', 'POST'])
def home():
    print("Background image URL:", BGIMG_URL)
    app.logger.info("Background image URL: %s", BGIMG_URL)
    return render_template('addemp.html', background=BGIMG, ownName=OWN_NAME)

@app.route("/about", methods=['GET','POST'])
def about():
    print("Background image URL:", BGIMG_URL)
    app.logger.info("Background image URL: %s", BGIMG_URL)
    return render_template('about.html', background=BGIMG, ownName=OWN_NAME)
    
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

  
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name

    finally:
        cursor.close()

    print("all modification done...")
    print("Background image URL:", BGIMG_URL)
    app.logger.info("Background image URL: %s", BGIMG_URL)
    return render_template('addempoutput.html', name=emp_name, background=BGIMG, ownName=OWN_NAME)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    print("Background image URL:", BGIMG_URL)
    app.logger.info("Background image URL: %s", BGIMG_URL)
    return render_template("getemp.html", background=BGIMG, ownName=OWN_NAME)


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        # Add No Employee found form
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()
        
    print("Background image URL:", BGIMG_URL)
    app.logger.info("Background image URL: %s", BGIMG_URL)
    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], background=BGIMG, ownName=OWN_NAME)

if __name__ == '__main__':
    
    # Check for Command Line Parameters for color
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    args = parser.parse_args()

    app.run(host='0.0.0.0',port=81,debug=True)
