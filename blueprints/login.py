from flask import Blueprint
from flask import jsonify, request
from config.dbUtils import get_database_connection

# Blueprint for the login component
login_bp = Blueprint('login', __name__)