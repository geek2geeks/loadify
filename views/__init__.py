# File: views\__init__.py

from flask import Blueprint

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
upload = Blueprint('upload', __name__)

