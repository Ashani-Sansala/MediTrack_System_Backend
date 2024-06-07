from flask import Blueprint, jsonify, request
from config.dbUtils import get_database_connection

manageUsers_bp = Blueprint('manageUsers', __name__)

@manageUsers_bp.route('/search', methods=['GET'])
def search_user():
    query = request.args.get('name', '')
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE name LIKE %s", (f"%{query}%",))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@manageUsers_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User deleted successfully"})

@manageUsers_bp.route('/add', methods=['POST'])
def add_user():
    data = request.get_json()
    conn = get_database_connection()
    cursor = conn.cursor()
    query = ("INSERT INTO users (employee_id, name, email, phone_number, register_as, position) "
             "VALUES (%s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (data['employee_id'], data['name'], data['email'], data['phone_number'], data['register_as'], data['position']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User added successfully"})
