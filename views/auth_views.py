# This file is located at /views/auth_views.py

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from models import User, db

def init_app(auth_blueprint):
    # Route for login page
    @auth_blueprint.route('/login', methods=['GET', 'POST'])
    def login():
        # If form is submitted
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            # Query the user
            user = User.query.filter_by(username=username).first()
            # If user exists and password is correct
            if user and user.check_password(password):
                # Log the user in
                login_user(user)
                # Redirect to home page
                return redirect(url_for('main.home'))
            else:
                # If credentials are invalid, show an error message
                flash('Invalid credentials', 'danger')
                return redirect(url_for('auth.login'))
        # Render login page
        return render_template('login.html')

    # Route for logout
    @auth_blueprint.route('/logout')
    @login_required  # User must be logged in to access this route
    def logout():
        # Log the user out
        logout_user()
        # Redirect to login page
        return redirect(url_for('auth.login'))

    # Route for register page
    @auth_blueprint.route('/register', methods=['GET', 'POST'])
    def register():
        # If form is submitted
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

        # Render register page
        return render_template('register.html')
