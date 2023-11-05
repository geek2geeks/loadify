#views\auth.py

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import auth
from models import User, db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate user input
        if not username or not password or not confirm_password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'danger')
            return render_template('register.html')

        # Create new user
        new_user = User(username=username)
        new_user.set_password(password)  # Hashes the password
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')
