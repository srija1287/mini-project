from flask import Flask,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from random import *  
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import tensorflow as tf
import tensorflow as tf
from email import message
import smtplib as s
import random

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.2
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
# Keras
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename


local_server= True
app = Flask(__name__)
app.secret_key='fakeface'

# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/ffdb'
db = SQLAlchemy(app)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)






@app.route("/")
def home():
    return render_template("home.html")






@app.route("/menu2")
def menu2():
    return render_template("menu2.html")


@app.route("/signup",methods=['POST','GET'])
def signup():
    if request.method=='POST':
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        user=User.query.filter_by(email=email).first()
        if user:
            print("user already Exist")
            return render_template("/signup.html",a="Email Already Exist")

        new_user=db.engine.execute(f"INSERT INTO `user`(`username`,`email`,`password`)VALUES('{username}','{email}','{password}')")
        captcha_code = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for i in range(5)])
        print(captcha_code)
        return render_template("/login.html",code=captcha_code)   
    return render_template("signup.html")

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST':
        user_captcha_code = request.form['captcha_code']
        captcha_code = request.form['captcha']
        print(captcha_code )
        email=request.form.get("email")
        password=request.form.get("password")
        user=User.query.filter_by(email=email,password=password).first()
        if user and password and user_captcha_code == captcha_code:
            login_user(user)
            return render_template("/menu.html")
        else:
            captcha_code = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for i in range(5)])
            print(captcha_code)
            return render_template("/login.html",a="Invaild username & password", code=captcha_code)
    else:
        captcha_code = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for i in range(5)])
        print(captcha_code)
        return render_template("login.html", code=captcha_code)

# Model saved with Keras model.save()
MODEL_PATH ='model.h5'

# Load your trained model
model = load_model(MODEL_PATH)




def model_predict(img_path, model):
    print(img_path)
    img = image.load_img(img_path, target_size=(300, 300))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
   

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
   # x = preprocess_input(x)

    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    if preds==0:
        preds="Fake Face Detected"

    elif preds==1:
        preds="Real Face Detected"
    
  
    
    
    
    return preds

 
@app.route("/prediction",methods=['POST','GET'])
def prediction():
    return render_template("prediction.html")

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None





    
    



if __name__ == "__main__":
    app.run(debug=True,use_reloader=True)