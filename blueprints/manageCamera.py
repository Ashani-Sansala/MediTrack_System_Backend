from flask import Blueprint, jsonify, request
from config.dbUtils import get_database_connection

manageCamera_bp = Blueprint('manageCamera', __name__)


@manageCamera_bp.route('/cameras', methods=['GET'])
def get_cameras():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cameras")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    cameras = []
    for row in rows:
        cameras.append({"CameraID": row[0], "Location": row[1]})

    return jsonify(cameras)


@manageCamera_bp.route('/add_camera', methods=['POST'])
def add_camera():
    data = request.json
    location = data['Location']

    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Cameras (Location) VALUES (%s)", (location,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Camera added successfully!"}), 201


@manageCamera_bp.route('/remove_camera/<int:camera_id>', methods=['DELETE'])
def remove_camera(camera_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Cameras WHERE CameraID = %s", (camera_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Camera removed successfully!"}), 200
