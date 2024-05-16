from flask import Blueprint, jsonify, request
from config.dbUtils import get_database_connection

# Blueprint for the login component
login_bp = Blueprint('login', __name__)

@login_bp.route('/test', methods=['GET'])
def test_connection():
    try:
        # Establish a connection to the database
        connection = get_database_connection()
        cursor = connection.cursor()

        # Query the database to select all records from the User table
        query = "SELECT * FROM User"
        cursor.execute(query)
        users = cursor.fetchall()

        # Close the cursor and database connection
        cursor.close()
        connection.close()

        # Prepare the output in JSON format
        output = [{"user_id": user[0], "username": user[1]} for user in users]

        return jsonify({"success": True, "message": "Database connectivity test successful", "users": output})
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@login_bp.route('/authenticate', methods=['POST'])
def authenticate_user():
    print("Request received at /login/authenticate")  # Print message when request is received
    
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    print("Received username:", username)  # Print received username
    print("Received password:", password)  # Print received password

    # Query the database to check if the user exists and the password is correct
    connection = get_database_connection()
    cursor = connection.cursor()

    query = "SELECT username, password FROM User WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user:
        # If user exists, check if the password matches
        if password == user[1]:
            print("Login successful")  # Print message for successful login
            return jsonify({"success": True, "message": "Login successful"})
        else:
            print("Invalid password")  # Print message for invalid password
            return jsonify({"success": False, "message": "Invalid password"})
    else:
        print("User not found")  # Print message for user not found
        return jsonify({"success": False, "message": "User not found"})

    # Close the cursor and database connection
    cursor.close()
    connection.close()