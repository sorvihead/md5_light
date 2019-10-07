from flask import Blueprint

bp = Blueprint('secure', __name__)

from app.secure_api import routes
