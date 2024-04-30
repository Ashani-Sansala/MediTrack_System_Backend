from flask import Blueprint
from flask import jsonify, request
from config.dbUtils import get_database_connection

# Blueprint for the manage users component
manageUsers_bp = Blueprint('manageUsers', __name__)