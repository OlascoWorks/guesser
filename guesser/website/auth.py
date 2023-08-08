from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('pass')

        user = User.query.filter_by(name=name).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully👍', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Password Incorrect☹', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('User does not exist', category='error')
            return redirect(url_for('auth.login'))

    return render_template('login.html', user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name').lower()
        password = request.form.get('pass')

        user = User.query.filter_by(name=name).first()
        if user:
            flash('A user with this name already exists☹', category='error')
        else:
            if len(name) < 3:
                flash('Name should be at least 3 characters', category='error')
            elif len(password) < 4:
                flash('Password should be at least 4 characters', category='error')
            else:
                new_user = User(name=name, password=generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account has been created successfully👍', category='success')
                return redirect(url_for('views.home'))


    return render_template('sign-up.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))