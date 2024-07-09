from flask import Blueprint, jsonify, request
from utils.dbConn import get_database_connection

# Blueprint for the dashboard component
historical_records_bp = Blueprint('historicalRecords', __name__)

# Route to get Equipment options for the search functionality
@historical_records_bp.route('/equipment-options', methods=['GET'])
def get_equipment_options():
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT eqpName FROM equipment ORDER BY eqpName ASC')
    equipment_names = [item[0] for item in cursor.fetchall()]
    cursor.close()
    connection.close()
    return jsonify(equipment_names)

# Route to get Building options for the search functionality
@historical_records_bp.route('/building-options', methods=['GET'])
def get_building_options():
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT buildingName FROM location ORDER BY buildingName ASC')
    building_names = [item[0] for item in cursor.fetchall()]
    cursor.close()
    connection.close()
    return jsonify(building_names)

# Route to get Floor options for the search functionality
@historical_records_bp.route('/floor-options', methods=['GET'])
def get_floor_options():
    buildings = request.args.get('buildings')
    connection = get_database_connection()
    cursor = connection.cursor()
    
    if buildings:
        buildings_list = buildings.split(',')
        query = f"SELECT DISTINCT floorNo FROM location WHERE buildingName IN ({','.join(['%s']*len(buildings_list))}) ORDER BY floorNo ASC"
        cursor.execute(query, buildings_list)
    else:
        cursor.execute('SELECT DISTINCT floorNo FROM location ORDER BY floorNo ASC')
    
    floor_numbers = [item[0] for item in cursor.fetchall()]
    cursor.close()
    connection.close()
    return jsonify(floor_numbers)

# Route to get Area options for the search functionality
@historical_records_bp.route('/area-options', methods=['GET'])
def get_area_options():
    buildings = request.args.get('buildings')
    floors = request.args.get('floors')
    connection = get_database_connection()
    cursor = connection.cursor()
    
    query = 'SELECT DISTINCT areaName FROM location'
    filters = []
    params = []
    
    if buildings:
        buildings_list = buildings.split(',')
        filters.append(f"buildingName IN ({','.join(['%s']*len(buildings_list))})")
        params.extend(buildings_list)
        
    if floors:
        floors_list = floors.split(',')
        filters.append(f"floorNo IN ({','.join(['%s']*len(floors_list))})")
        params.extend(floors_list)
    
    if filters:
        query += ' WHERE ' + ' AND '.join(filters)
    
    query += ' ORDER BY areaName ASC'
    
    cursor.execute(query, params)
    area_names = [item[0] for item in cursor.fetchall()]
    cursor.close()
    connection.close()
    return jsonify(area_names)

# Route to get data for the Location table
@historical_records_bp.route('/table', methods=['GET', 'POST'])
def get_table():
    connection = get_database_connection()
    cursor = connection.cursor()

    # Build the query based on the search terms
    #query = 'SELECT dl.logId, e.eqpName, l.buildingName, l.floorNo, l.areaName, dl.detectionTime, dl.videoPath FROM detectionLogs dl JOIN equipment e ON dl.eqpId = e.eqpId JOIN location l ON dl.locId = l.locId'

    #query = 'CALL GetDetectionLogs()'

    query = ('SELECT dl.logId, e.eqpName, l.buildingName, l.floorNo, l.areaName, '
        'dl.detectionDate, dl.detectionTime, dl.videoPath '
        'FROM detectionLogs dl '
        'JOIN equipment e ON dl.eqpId = e.eqpId '
        'JOIN location l ON dl.locId = l.locId ')

    search_terms = request.args
    filters = []

    # For debugging purposes
    print(search_terms)

    for key, value in search_terms.items():
        start_date = search_terms.get('startDate')
        end_date = search_terms.get('endDate')
        if start_date and end_date:
            filters.append(f"detectionDate BETWEEN '{start_date}' AND '{end_date}'")
        if key == 'startTime' and 'endTime' in search_terms:
            start_time = search_terms.get('startTime')
            end_time = search_terms.get('endTime')
            filters.append(f"detectionTime BETWEEN '{start_time}' AND '{end_time}'")
        elif key == 'floorNo' and value:
            filters.append(f"{key} IN ({value})")
        elif key == 'eqpName' and value:
            filters.append(f"{key} REGEXP '{value.replace(',', '|')}'")
        elif key == 'buildingName' and value:
            filters.append(f"{key} REGEXP '{value.replace(',', '|')}'")
        elif key == 'areaName' and value:
            filters.append(f"{key} REGEXP '{value.replace(',', '|')}'")
    
    if filters:
        query += ' WHERE ' + ' AND '.join(filters)

    query += ' ORDER BY dl.logId DESC'

    # For debugging purposes
    print(query)

    cursor.execute(query)
    results = cursor.fetchall()

    # Convert results to JSON serializable format
    serializable_results = []
    for row in results:
        serializable_row = list(row)
        
        # Convert timedelta to seconds (integer)
        serializable_row[6] = int(serializable_row[6].total_seconds())
        serializable_results.append(serializable_row)
        

    print(serializable_results)
    cursor.close()
    connection.close()
    return jsonify(serializable_results)
