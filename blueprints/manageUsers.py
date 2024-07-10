from flask import Blueprint, jsonify, request
from utils.dbConn import get_database_connection
from utils.encryption import decrypt, hash_password
from mysql.connector import Error

# Blueprint for managing users
manageUsers_bp = Blueprint('manageUsers', __name__)

# Route to get user data based on a search term
@manageUsers_bp.route('/getData', methods=['GET'])
def get_user():
    search = request.args.get('search', '')  # Get the search term from query parameters
    conn = get_database_connection()  # Establish a database connection
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.callproc('GetUserData', (search,))  # Call stored procedure to get user data
            for result in cursor.stored_results():
                results = result.fetchall()  # Fetch the results from the stored procedure
        return jsonify(results), 200  # Return the results as a JSON response
    except Error as e:
        return jsonify({'error': str(e)}), 500  # Handle database errors
    finally:
        conn.close()  # Ensure the database connection is closed

# Route to remove a user by username
@manageUsers_bp.route('/remove/<username>', methods=['DELETE'])
def remove_user(username):
    conn = get_database_connection()  # Establish a database connection
    try:
        with conn.cursor() as cursor:
            cursor.callproc('RemoveUser', (username,))  # Call stored procedure to remove a user
        conn.commit()  # Commit the transaction
        return jsonify({'message': 'User removed successfully'}), 200  # Return a success message
    except Error as e:
        conn.rollback()  # Rollback the transaction in case of an error
        return jsonify({'error': str(e)}), 500  # Handle database errors
    finally:
        conn.close()  # Ensure the database connection is closed

# Route to add a new user
@manageUsers_bp.route('/add', methods=['POST'])
def add_user():
    data = request.json  # Get the JSON data from the request body
    print(data)  # Print data for debugging purposes
    conn = get_database_connection()  # Establish a database connection
    try:
        # Decrypt sensitive information
        password = decrypt(data['password'], data['passIv'])
        email = decrypt(data['email'], data['emailIv'])
        phone_no = decrypt(data['phoneNo'], data['phoneNoIv'])
        hashed_password = hash_password(password)  # Hash the decrypted password

        with conn.cursor() as cursor:
            # Call stored procedure to add a new user
            cursor.callproc('AddUser', (
                data['username'],
                hashed_password,
                data['fullName'],
                data['birthday'],
                email,
                phone_no,
                data['pId']
            ))
        conn.commit()  # Commit the transaction
        return jsonify({'message': 'User added successfully'}), 201  # Return a success message
    except Error as e:
        print(f"Error: {str(e)}")  # Print the error for debugging purposes
        conn.rollback()  # Rollback the transaction in case of an error
        return jsonify({'error': str(e)}), 500  # Handle database errors
    finally:
        conn.close()  # Ensure the database connection is closed

# Route to get position data for users
@manageUsers_bp.route('/positionData', methods=['GET'])
def get_positions():
    conn = get_database_connection()  # Establish a database connection
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.callproc('GetPositions')  # Call stored procedure to get position data
            for result in cursor.stored_results():
                positions = result.fetchall()  # Fetch the results from the stored procedure
        return jsonify(positions), 200  # Return the position data as a JSON response
    except Error as e:
        return jsonify({'error': str(e)}), 500  # Handle database errors
    finally:
        conn.close()  # Ensure the database connection is closed

# Route to check if a username is available
@manageUsers_bp.route('/checkUsername', methods=['GET'])
def check_username():
    username = request.args.get('username')  # Get the username from query parameters
    conn = get_database_connection()  # Establish a database connection
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.callproc('CheckUsername', (username,))  # Call stored procedure to check username availability
            for result in cursor.stored_results():
                count = result.fetchone()['count']  # Get the count of existing usernames
        available = count == 0  # Check if the username is available
        return jsonify({'available': available}), 200  # Return the availability status
    except Error as e:
        return jsonify({'error': str(e)}), 500  # Handle database errors
    finally:
        conn.close()  # Ensure the database connection is closed
