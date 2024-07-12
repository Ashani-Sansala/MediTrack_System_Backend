from flask import Blueprint, jsonify, request
from utils.dbConn import get_database_connection
from utils.encryption import decrypt, verify_password
from mysql.connector import Error

# Blueprint for the login component
login_bp = Blueprint('login', __name__)

# Route to authenticate user credentials
@login_bp.route('/authenticate', methods=['POST'])
def authenticate_user():
    data = request.json
    # Check if request data is present
    if not data:
        return jsonify({"success": False, "message": "Invalid request"}), 400

    # List of required fields for authentication
    required_fields = ['username', 'password', 'unameIv', 'passIv']
    # Ensure all required fields are present in the request data
    if not all(field in data for field in required_fields):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    try:
        # Decrypt the received username and password
        username = decrypt(data['username'], data['unameIv'])
        password = decrypt(data['password'], data['passIv'])
    except Exception as e:
        return jsonify({"success": False, "message": "Decryption failed"}), 400

    # Establish a database connection
    connection = get_database_connection()
    try:
        with connection.cursor(dictionary=True) as cursor:
            # Call stored procedure to get user information by username
            cursor.callproc('AuthenticateUser', (username,))
            for result in cursor.stored_results():
                user = result.fetchone()

        # If user is found in the database
        if user:
            # Verify the password
            if verify_password(user['password'], password):
                return jsonify({
                    "success": True, 
                    "message": "Login successful", 
                    "username": user['username'], 
                    "fullName": user['fullName'], 
                    "category": user['category'], 
                    "avatarUrl": user['avatarUrl']
                })
            else:
                return jsonify({"success": False, "message": "Invalid credentials"}), 401
        else:
            return jsonify({"success": False, "message": "User not found"}), 404
    except Error as e:
        # Handle any database errors
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        # Close the database connection
        connection.close()
