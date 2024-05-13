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

        # Output the records in the terminal
        for user in users:
            print(user)

        # Close the cursor and database connection
        cursor.close()
        connection.close()

        return jsonify({"success": True, "message": "Database connectivity test successful"})
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
