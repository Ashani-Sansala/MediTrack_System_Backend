from flask import Blueprint
from flask import jsonify, request
from config.dbUtils import get_database_connection

# Blueprint for the dashboard component
dashboard_bp = Blueprint('dashboard', __name__)