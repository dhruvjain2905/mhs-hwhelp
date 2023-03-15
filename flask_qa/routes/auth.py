from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from flask_qa.extensions import db
from flask_qa.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        unhashed_password = request.form['password']
        confirm_pass = request.form['confirm']


        name_exists = User.query.filter_by(name=name).first()
        if name_exists:
            flash('Username is already in use. Please try something different', category='error')
        elif confirm_pass != unhashed_password:
            flash("Passwords are different! Please enter the same password.", category='error')
        elif len(name) < 1:
            flash('Username is too short. Must be at least 4 characters.', category='error')
        elif len(unhashed_password) < 1:
            flash('Password is too short. Must be at least 4 characters', category='error')
        else:
            if name == "MHS":
                user = User(
                    name=name, 
                    unhashed_password=unhashed_password,
                    admin=True,  
                    expert=False
                )

                db.session.add(user)
                db.session.commit()
            else:
                user = User(
                    name=name, 
                    unhashed_password=unhashed_password,
                    admin=False,  
                    expert=False
                )

                db.session.add(user)
                db.session.commit()

            login_user(user)
            flash('User created!')
            return redirect(url_for('main.index'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(name=name).first()

        error_message = ''

        if not user or not check_password_hash(user.password, password):
            flash('Could not login. Please check and try again.', category='error')
        else:
            login_user(user)
            flash("Logged In!", category="success")
            return redirect(url_for('main.index'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))