from flask import Blueprint, jsonify, request
from utils.dbConn import get_database_connection
from utils.encryption import decrypt, verify_password

# Blueprint for the login component
login_bp = Blueprint('login', __name__)

@login_bp.route('/authenticate', methods=['POST'])
def authenticate_user():
    data = request.json
    print(data)
    if not data:
        return jsonify({"success": False, "message": "Invalid request"}), 400

    encrypted_username = data.get('username')
    encrypted_password = data.get('password')
    uname_iv = data.get('unameIv')
    pass_iv = data.get('passIv')

    if not (encrypted_username and encrypted_password and uname_iv and pass_iv):
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    
    print(encrypted_username)
    print(encrypted_password)
    print(uname_iv)
    print(pass_iv)

    try:
        # Decrypt the received username and password
        username = decrypt(encrypted_username, uname_iv)
        password = decrypt(encrypted_password, pass_iv)
    except Exception as e:
        return jsonify({"success": False, "message": "Decryption failed"}), 400

    # Query the database to check if the user exists and the password is correct
    connection = get_database_connection()
    cursor = connection.cursor()

    query = "SELECT username, password, fullName, pId FROM User WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:
        if verify_password(user[1], password):
            # Return the user's name in the response
            return jsonify({"success": True, "message": "Login successful", "username": user[0], "fullName": user[2], "pID": user[3]})
        else:
            return jsonify({"success": False, "message": "Invalid password"}), 401
    else:
        return jsonify({"success": False, "message": "User not found"}), 404

# Additional security headers
@login_bp.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
