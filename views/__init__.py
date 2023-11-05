# File: views\__init__.py

from flask import Blueprint

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
upload = Blueprint('upload', __name__)

# Importing the blueprints after their declaration to avoid circular imports
from . import main
from . import auth
from . import upload

