from flask import Blueprint, jsonify, request
from utils.dbConn import get_database_connection
from mysql.connector import Error

# Blueprint for the manage camera component
manageCamera_bp = Blueprint('manageCamera', __name__)

# Route to get camera data based on a search term
@manageCamera_bp.route('/getData', methods=['GET'])
def get_camera():
    search_term = request.args.get('search', '')  # Get the search term from query parameters
    conn = get_database_connection()  # Establish a database connection
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.callproc('GetCameraData', (search_term,))  # Call stored procedure to get camera data
            for result in cursor.stored_results():
                data = result.fetchall()  # Fetch the results from the stored procedure
        return jsonify(data)  # Return the data as a JSON response
    except Error as e:
        return jsonify({'error': str(e)}), 500  # Handle database errors
    finally:
        conn.close()  # Ensure the database connection is closed

# Route to add a new camera
@manageCamera_bp.route('/add', methods=['POST'])
def add_camera():
    data = request.json  # Get the JSON data from the request body
    conn = get_database_connection()  # Establish a database connection
    try:
        with conn.cursor() as cursor:
            cursor.callproc('AddCamera', (
                data.get('locId'),
                data.get('ipAddress'),
                data.get('model'),
                data.get('installationDate'),
                data.get('cameraStatus')
            ))  # Call stored procedure to add a new camera
            for result in cursor.stored_results():
                camera_id = result.fetchone()[0]  # Fetch the newly added camera ID
        conn.commit()  # Commit the transaction
        return jsonify({'success': True, 'message': 'Camera added successfully', 'cameraId': camera_id}), 201
    except Error as e:
        conn.rollback()  # Rollback the transaction in case of an error
        return jsonify({'error': str(e)}), 500  # Handle database errors
    finally:
        conn.close()  # Ensure the database connection is closed

# Route to update an existing camera
@manageCamera_bp.route('/updateCamera/<int:cameraId>', methods=['PUT'])
def update_camera(cameraId):
    data = request.json  # Get the JSON data from the request body
    conn = get_database_connection()  # Establish a database connection
    try:
        with conn.cursor() as cursor:
            cursor.callproc('UpdateCamera', (
                cameraId,
                data['ipAddress'],
                data['cameraStatus']
            ))  # Call stored procedure to update camera details
        conn.commit()  # Commit the transaction
        return jsonify({'success': True, 'message': 'Camera updated successfully'}), 200
    except Error as e:
        conn.rollback()  # Rollback the transaction in case of an error
        return jsonify({'error': str(e)}), 500  # Handle database errors
    finally:
        conn.close()  # Ensure the database connection is closed

# Route to get location data for cameras
@manageCamera_bp.route('/locationData', methods=['GET'])
def get_locations():
    conn = get_database_connection()  # Establish a database connection
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.callproc('GetLocationData')  # Call stored procedure to get location data
            for result in cursor.stored_results():
                locations = result.fetchall()  # Fetch the results from the stored procedure
        return jsonify(locations)  # Return the location data as a JSON response
    except Error as e:
        return jsonify({'error': str(e)}), 500  # Handle database errors
    finally:
        conn.close()  # Ensure the database connection is closed