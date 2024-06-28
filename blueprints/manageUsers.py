from flask import Blueprint, jsonify, request, make_response
from utils.dbConn import get_database_connection
from utils.encryption import decrypt, hash_password

manageUsers_bp = Blueprint('manageUsers', __name__)

@manageUsers_bp.route('/getData', methods=['GET'])
def get_user():
    search = request.args.get('search', '')
    search_term = f"%{search}%"
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)

    query = ("""SELECT 
                u.username,
                u.fullName,
                DATE_FORMAT(u.birthday, '%Y-%m-%d') AS birthday,
                u.email,
                u.phoneNo,
                p.positionName,
                p.pId
            FROM 
                user u
            JOIN 
                position p ON u.pId = p.pId
            WHERE 
                u.username LIKE %s OR 
                u.fullName LIKE %s OR 
                u.birthday LIKE %s OR 
                u.email LIKE %s OR 
                u.phoneNo LIKE %s OR 
                p.positionName LIKE %s""")
    
    cursor.execute(query, (search_term, search_term, search_term, search_term, search_term, search_term))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results), 200

@manageUsers_bp.route('/remove/<username>', methods=['DELETE'])
def remove_user(username):
    conn = get_database_connection()
    cursor = conn.cursor()
    query = "DELETE FROM user WHERE username = %s"
    cursor.execute(query, (username,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'User removed successfully'}), 200

@manageUsers_bp.route('/add', methods=['POST'])
def add_user():
    data = request.json
    conn = get_database_connection()
    cursor = conn.cursor()

    username = data['username']
    encrypted_password = data['password']
    full_name = data['fullName']
    birthday = data['birthday']
    encrypted_email = data['email']
    encrypted_phone_no = data['phoneNo']
    pId = data['pId']

    pass_iv = data['passIv']
    email_iv = data['emailIv']
    phone_no_iv = data['phoneNoIv']

    password = decrypt(encrypted_password, pass_iv)
    email = decrypt(encrypted_email, email_iv)
    phone_no = decrypt(encrypted_phone_no, phone_no_iv)

    hashed_password = hash_password(password)
    
    query = ("INSERT INTO user (username, password, fullName, birthday, email, phoneNo, pId) "
             "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (username, hashed_password, full_name, birthday, 
                           email, phone_no, pId))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'User added successfully'}), 201

@manageUsers_bp.route('/positionData', methods=['GET'])
def get_positions():
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT pId, positionName FROM position")
    positions = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(positions), 200

@manageUsers_bp.route('/checkUsername', methods=['GET'])
def check_username():
    username = request.args.get('username')
    conn = get_database_connection()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM user WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    available = result[0] == 0
    return jsonify({'available': available}), 200
