from flask import Blueprint
from flask import jsonify, request
from config.dbUtils import get_database_connection

# Blueprint for the manage camera component
manageCamera_bp = Blueprint('manageCamera', __name__)