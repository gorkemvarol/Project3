# import necessary libraries
from json import load
from models import create_classes
import os
import sqlite3
from flask import Flask, redirect, render_template,url_for, request
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import numpy as np
# from flask import (
#     Flask,
#     render_template,
#     jsonify,
#     request,
#     redirect,
#     url_for)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


model = load_model('heart_prediction_model.h5')
#################################################
# Database Setup
#################################################

# from flask_sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///app.db"

# # Remove tracking modifications
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# Patient = create_classes(db)

# create route that renders index.html template
@app.route("/")
def home():
    print ("inside route /")
    return render_template("index.html")


# Query the database and send the jsonified results
@app.route("/send", methods=["POST","GET" ])
def send():
    print("inside route /send")
    if request.method == "POST":
        age = request.form["age"]
        sex = request.form["sex"]
        cp = request.form["cp"]
        trestbps = request.form["restbpm"]
        chol = request.form["chol"]
        fbs = request.form["fbs"]
        restecg = request.form["ecg"]
        thalach = request.form["maxhr"]
        exang = request.form["exang"]
        oldpeak = request.form["oldpeak"]
        slope = request.form["slope"]
        ca = request.form["ca"]

        # patient = Patient(age=age, sex = sex, cp = cp,trestbps=trestbps,
        # chol=chol,fbs=fbs,restecg=restecg,thalach=thalach,exang=exang,oldpeak=oldpeak,slope=slope,ca=ca)
        # db.session.add(patient)
        # db.session.commit()

          # call the method to store the data in database(sqlite)
        store_patient(age, sex, cp, trestbps,chol, fbs, restecg, thalach, exang, oldpeak, slope, ca)

        x = np.zeros( (1,12) )
        
        x[0,0] = age
        x[0,1] = sex
        x[0,2] = cp
        x[0,3] = trestbps
        x[0,4] = chol
        x[0,5] = fbs
        x[0,6] = restecg
        x[0,7] = thalach
        x[0,8] = exang
        x[0,9] = oldpeak
        x[0,10] = slope
        x[0,11] = ca
        # pred = model.predict(x)
        predict_classes = model.predict_classes(x)
        print(predict_classes)
        if predict_classes == 1:
            disease_type = 'Absent'
        elif predict_classes == 2:
            disease_type = 'a Fixed Defect'
        elif predict_classes == 3:
            disease_type = 'a Reversable Defect'
        print(disease_type)
        # return redirect(url_for('patients'))
        return redirect(url_for('patients', disease_type= disease_type))
    return render_template('form.html')
        # return redirect(url_for('/'))
   


        # return render_template("form.html")


@app.route("/patients/<disease_type>")
def patients(disease_type):

    return render_template('disease.html', disease_type = disease_type)



################## Function ##########

def store_patient(age, sex, cp, trestbps,chol, fbs, restecg, thalach, exang, oldpeak, slope, ca):
    print("hello")
    working_directory = os.getcwd() + '/'+'app.db'
    connection = sqlite3.connect(working_directory)
    # connection = sqlite3.connect("C:/Users/vijay/Documents/Saradha_R/project3/project3/deploy/app.db") 
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
    insert into patients
    values (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (age, sex, cp, trestbps,chol, fbs, restecg, thalach, exang, oldpeak, slope, ca))
  

    connection.commit()
    connection.close()
    return ""


##########


if __name__ == "__main__":
    app.run(debug= True)
