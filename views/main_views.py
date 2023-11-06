# This file is located at /views/main_views.py

from flask import render_template

def init_app(main_blueprint):
    # Route for the home page
    @main_blueprint.route('/')
    def home():
        # Render the home page
        return render_template('index.html')
