from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__) # same as filename (optional)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash("An account with that email doesn't exist, please try again.", category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('An account already exists with this email address.', category="error")
        elif len(email) < 4:
            flash('Invalid email', category="error")
        elif len(firstName) < 2:
            flash('Invalid name', category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        elif len(password1) < 8:
            flash("Password must be atleast 8 characters", category="error")
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully", category="success")
            login_user(new_user, remember=True)
            return redirect(url_for('views.dashboard'))

    return render_template("sign_up.html", user=current_user)
