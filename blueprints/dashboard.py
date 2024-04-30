from flask import Blueprint
from flask import jsonify, request
from config.dbUtils import get_database_connection

# Blueprint for the dashboard component
dashboard_bp = Blueprint('dashboard', __name__)

# Route to get Equipment options for the search functionality
@dashboard_bp.route('/equipment-options', methods=['GET'])
def get_equipment_options():
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT eqpName FROM location ORDER BY eqpName ASC')
    equipment_names = [item[0] for item in cursor.fetchall()]
    cursor.close()
    connection.close()

    print(equipment_names)
    return jsonify(equipment_names)

# Route to get Floor options for the search functionality
@dashboard_bp.route('/floor-options', methods=['GET'])
def get_floor_options():
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT floor FROM location ORDER BY floor ASC')
    floor_numbers = [item[0] for item in cursor.fetchall()]
    cursor.close()
    connection.close()
    
    print(floor_numbers)
    return jsonify(floor_numbers)

# Route to get data for the Location table
@dashboard_bp.route('/table', methods=['GET', 'POST'])
def get_table():
    connection = get_database_connection()
    cursor = connection.cursor()

    # Build the query based on the search terms
    query = 'SELECT * FROM location'

    search_terms = request.args
    filters = []

    # For debugging purposes
    print(search_terms)

    for key, value in search_terms.items():
        if key in ['area', 'time_'] and value:
            filters.append(f"{key} LIKE '%{value}%'")
        elif key == 'floor' and value:
            filters.append(f"{key} IN ({value})")
        elif key == 'eqpName' and value:
            filters.append(f"{key} REGEXP '{value.replace(',', '|')}'")
    
    if filters:
        query += ' WHERE ' + ' AND '.join(filters)

    # For debugging purposes
    print(query)

    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(results)