from flask import Blueprint, jsonify, request
from utils.dbConn import get_database_connection

# Blueprint for the dashboard component
dashboard_bp = Blueprint('dashboard', __name__)

# Route to get Equipment options for the search functionality
@dashboard_bp.route('/equipment-options', methods=['GET'])
def get_equipment_options():
    # Establish a database connection
    connection = get_database_connection()
    cursor = connection.cursor()
    
    # Call stored procedure to get equipment options
    cursor.callproc('GetEquipmentOptions')
    
    # Fetch results from stored procedure and extract equipment names
    for result in cursor.stored_results():
        equipment_names = [item[0] for item in result.fetchall()]
    
    # Close cursor and connection
    cursor.close()
    connection.close()
    
    # Return equipment names as a JSON response
    return jsonify(equipment_names)

# Route to get Building options for the search functionality
@dashboard_bp.route('/building-options', methods=['GET'])
def get_building_options():
    # Establish a database connection
    connection = get_database_connection()
    cursor = connection.cursor()
    
    # Call stored procedure to get building options
    cursor.callproc('GetBuildingOptions')
    
    # Fetch results from stored procedure and extract building names
    for result in cursor.stored_results():
        building_names = [item[0] for item in result.fetchall()]
    
    # Close cursor and connection
    cursor.close()
    connection.close()
    
    # Return building names as a JSON response
    return jsonify(building_names)

# Route to get Floor options for the search functionality
@dashboard_bp.route('/floor-options', methods=['GET'])
def get_floor_options():
    # Get building names from request parameters
    buildings = request.args.get('buildings')
    
    # Establish a database connection
    connection = get_database_connection()
    cursor = connection.cursor()
    
    # If buildings are specified, filter floors by those buildings
    if buildings:
        buildings_list = buildings.split(',')
        query = f"SELECT DISTINCT floorNo FROM location WHERE buildingName IN ({','.join(['%s']*len(buildings_list))}) ORDER BY floorNo ASC"
        cursor.execute(query, buildings_list)
    else:
        # Otherwise, get all distinct floor numbers
        cursor.execute('SELECT DISTINCT floorNo FROM location ORDER BY floorNo ASC')
    
    # Extract floor numbers from the query result
    floor_numbers = [item[0] for item in cursor.fetchall()]
    
    # Close cursor and connection
    cursor.close()
    connection.close()
    
    # Return floor numbers as a JSON response
    return jsonify(floor_numbers)

# Route to get Area options for the search functionality
@dashboard_bp.route('/area-options', methods=['GET'])
def get_area_options():
    # Get building and floor names from request parameters
    buildings = request.args.get('buildings')
    floors = request.args.get('floors')
    
    # Establish a database connection
    connection = get_database_connection()
    cursor = connection.cursor()
    
    # Start building the query to get area names
    query = 'SELECT DISTINCT areaName FROM location'
    filters = []
    params = []
    
    # If buildings are specified, add them to the filter
    if buildings:
        buildings_list = buildings.split(',')
        filters.append(f"buildingName IN ({','.join(['%s']*len(buildings_list))})")
        params.extend(buildings_list)
    
    # If floors are specified, add them to the filter
    if floors:
        floors_list = floors.split(',')
        filters.append(f"floorNo IN ({','.join(['%s']*len(floors_list))})")
        params.extend(floors_list)
    
    # Combine filters and complete the query
    if filters:
        query += ' WHERE ' + ' AND '.join(filters)
    query += ' ORDER BY areaName ASC'
    
    # Execute the query with the parameters
    cursor.execute(query, params)
    
    # Extract area names from the query result
    area_names = [item[0] for item in cursor.fetchall()]
    
    # Close cursor and connection
    cursor.close()
    connection.close()
    
    # Return area names as a JSON response
    return jsonify(area_names)

# Route to get data for the Location table
@dashboard_bp.route('/table', methods=['GET', 'POST'])
def get_table():
    # Establish a database connection
    connection = get_database_connection()
    cursor = connection.cursor()
    
    # Get search terms from request parameters
    search_terms = request.args
    start_time = search_terms.get('startTime')
    end_time = search_terms.get('endTime')
    floor_no = search_terms.get('floorNo')
    eqp_name = search_terms.get('eqpName')
    building_name = search_terms.get('buildingName')
    area_name = search_terms.get('areaName')
    
    # Call stored procedure to get table data based on search terms
    cursor.callproc('GetTableData', (start_time, end_time, floor_no, eqp_name, building_name, area_name))
    
    # Fetch results from stored procedure
    for result in cursor.stored_results():
        results = result.fetchall()
    
    # Convert results to JSON serializable format
    serializable_results = []
    for row in results:
        serializable_row = list(row)
        # Convert timedelta to seconds (integer)
        serializable_row[6] = int(serializable_row[6].total_seconds())
        serializable_results.append(serializable_row)
    
    # Close cursor and connection
    cursor.close()
    connection.close()
    
    # Return table data as a JSON response
    return jsonify(serializable_results)
