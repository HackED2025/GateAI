from flask import Blueprint, flash, render_template, request, url_for, Response
from flask_login import login_required, current_user
from .models import Note
from . import db
from .facial_recognition import facial_recognition
import os

views = Blueprint('views', __name__) # same as filename (optional)
log = [] 

@views.route('/', methods=['GET','POST']) # / route aka main page
def home():
    return render_template("home.html")

@views.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    log = []
    if os.path.exists("detection_log.txt"):
        with open("detection_log.txt", "r") as log_file:
            log = log_file.readlines()
    return render_template("dashboard.html", user=current_user, log=log)

@views.route('/video_feed')
@login_required
def video_feed():

    return Response(facial_recognition(), mimetype='multipart/x-mixed-replace; boundary=frame')
