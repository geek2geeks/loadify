from views import main_views, auth_views, upload_views
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models import db, User

# Initialize Flask application
app = Flask(__name__)
# Load configuration from Config class
app.config.from_object(Config)
# Initialize SQLAlchemy with app
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# User loader callback for Flask-Login


@login_manager.user_loader
def load_user(user_id):
    # Load user by ID
    return User.query.get(int(user_id))


# Define blueprints here instead of 'views/__init__.py'
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
upload = Blueprint('upload', __name__)

# Import views modules here to associate them with the blueprints
# It is important that this is done after the blueprints are created
# to avoid circular imports. Also, the blueprints are passed as an
# argument to avoid the import statements in the view modules themselves.

main_views.init_app(main)
auth_views.init_app(auth)
# Pass the app instance to upload_views.init_app
upload_views.init_app(upload, app)

# Register blueprints
app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(upload)

# Main entry point
if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    # Start Flask app
    app.run(debug=True)
