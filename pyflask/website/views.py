from flask import Blueprint, flash, render_template, request
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__) # same as filename (optional)

@views.route('/', methods=['GET','POST']) # / route aka main page
def home():
    return render_template("home.html")

@views.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note cannot be blank.', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added.', category='success')
    return render_template("dashboard.html", user=current_user)
