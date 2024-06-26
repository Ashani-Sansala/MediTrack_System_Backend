from flask import Blueprint, jsonify, request
from flask_cors import CORS
from config.dbUtils import get_database_connection
import re

manageCamera_bp = Blueprint('manageCamera', __name__)
CORS(manageCamera_bp)


def generate_camera_id():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(cameraId) FROM camera")
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    if result:
        # Extract numeric part from existing cameraId and increment
        numeric_part = int(re.search(r'\d+', result).group()) + 1
        new_camera_id = f'CAM{numeric_part:03}'
    else:
        new_camera_id = 'CAM001'

    return new_camera_id

@manageCamera_bp.route('/cameras', methods=['GET'])
def get_cameras():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM camera")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    cameras = [{"cameraId": row[0], "locId": row[1], "ipAddress": row[2], "model": row[3], "installationDate": row[4].strftime('%Y-%m-%d')} for row in rows]

    return jsonify(cameras)

@manageCamera_bp.route('/add_camera', methods=['POST'])
def add_camera():
    data = request.json
    location = data['locId']
    ip_address = data['ipAddress']
    model = data['model']
    installation_date = data['installationDate']

    # Check if location exists in the location table
    if not location_exists(location):
        return jsonify({"error": f"Location with locId '{location}' does not exist. Please create the location first."}), 400

    # Generate camera ID
    camera_id = generate_camera_id()

    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO camera (cameraId, locId, ipAddress, model, installationDate) VALUES (%s, %s, %s, %s, %s)",
                       (camera_id, location, ip_address, model, installation_date))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Camera added successfully!", "cameraId": camera_id}), 201
    except Exception as e:
        return jsonify({"error": f"Error adding camera: {str(e)}"}), 500

@manageCamera_bp.route('/add_location', methods=['POST'])
def add_location():
    data = request.json
    location_id = data['locId']

    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO location (locId) VALUES (%s)", (location_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Location added successfully!", "locId": location_id}), 201
    except Exception as e:
        return jsonify({"error": f"Error adding location: {str(e)}"}), 500

def location_exists(location_id):
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT locId FROM location WHERE locId = %s", (location_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking if location exists: {e}")
        return False

@manageCamera_bp.route('/remove_camera/<camera_id>', methods=['DELETE', 'OPTIONS'])
def remove_camera(camera_id):
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'DELETE')
        return response, 200

    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM camera WHERE cameraId = %s", (camera_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Camera removed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": f"Error removing camera: {str(e)}"}), 500