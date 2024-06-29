from flask import Blueprint, jsonify, request
from utils.dbConn import get_database_connection

manageCamera_bp = Blueprint('manageCamera', __name__)

@manageCamera_bp.route('/getData', methods=['GET'])
def get_camera():
    search_term = request.args.get('search', '')
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    query = ("""
            SELECT 
                c.cameraId, 
                c.ipAddress, 
                c.model, 
                c.installationDate, 
                l.buildingName, 
                l.floorNo, 
                l.areaName, 
                c.cameraStatus
            FROM 
                camera c
            JOIN 
                location l ON c.locId = l.locId
            WHERE 
                c.cameraId LIKE %s OR
                c.ipAddress LIKE %s OR
                c.model LIKE %s OR
                c.installationDate LIKE %s OR
                l.buildingName LIKE %s OR
                l.floorNo LIKE %s OR
                l.areaName LIKE %s OR
                c.cameraStatus LIKE %s;
            """)
    search_pattern = f"%{search_term}%"
    cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    print(data)
    return jsonify(data)

@manageCamera_bp.route('/add', methods=['POST'])
def add_camera():
    data = request.json
    loc_id = data.get('locId')
    ip_address = data.get('ipAddress')
    model = data.get('model')
    installation_date = data.get('installationDate')
    camera_status = data.get('cameraStatus')  

    print(data)
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO camera (locId, ipAddress, model, installationDate, cameraStatus)
        VALUES (%s, %s, %s, %s, %s)
    """, (loc_id, ip_address, model, installation_date, camera_status))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'success': True, 'message': 'Camera added successfully'}), 201


@manageCamera_bp.route('/updateCamera/<cameraId>', methods=['PUT'])
def update_camera(cameraId):
    data = request.json
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE camera SET ipAddress=%s, cameraStatus=%s WHERE cameraId=%s",
        (data['ipAddress'], data['cameraStatus'], cameraId)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Camera updated successfully'}), 200


@manageCamera_bp.route('/locationData', methods=['GET'])
def get_locations():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT locId, areaName, floorNo, buildingName FROM location ORDER BY buildingName, floorNo, areaName ASC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    locations = []
    for row in data:
        locations.append({
            'locId': row[0],
            'areaName': row[1],
            'floorNo': row[2],
            'buildingName': row[3]
        })
    return jsonify(locations)

