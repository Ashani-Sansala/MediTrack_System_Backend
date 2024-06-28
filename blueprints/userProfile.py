from flask import Blueprint, jsonify, request
from utils.dbConn import get_database_connection
from utils.encryption import decrypt, verify_password, hash_password

# Blueprint for the user profile component
userProfile_bp = Blueprint('userProfile', __name__)

@userProfile_bp.route('/getUserProfile', methods=['GET', 'POST'])
def get_user_profile():
    data = request.json
    username = str(data.get('username'))
    if not username:
        return jsonify({"success": False, "message": "User not logged in"}), 401
    
    connection = get_database_connection()
    cursor = connection.cursor()

    query = """
    SELECT u.username, u.fullName, 
    DATE_FORMAT(u.birthday, '%Y-%m-%d') AS birthday,
    u.email, u.phoneNo, p.positionName
    FROM user u
    JOIN position p ON u.pId = p.pId
    WHERE u.username = %s
    """
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:
        user_details = {
            "username": user[0],
            "fullName": user[1],
            "birthday": user[2],
            "email": user[3],
            "phone": user[4],
            "position": user[5]
        }

        print("get values : ", user_details)
        return jsonify({"success": True, "userDetails": user_details})
    else:
        return jsonify({"success": False, "message": "User not found"}), 404

@userProfile_bp.route('/updateUserProfile', methods=['POST'])
def update_user_profile():
    data = request.json
    print("update valuses : ", data)
    username = str(data.get('username'))
    if not username:
        return jsonify({"success": False, "message": "User not logged in"}), 401

    fullName = data.get('fullName')
    birthday = data.get('birthdate')
    email = data.get('email')
    phone = data.get('phone')
    position = data.get('position')

    print('\n Birthdate: ', birthday)

    connection = get_database_connection()
    cursor = connection.cursor()

    # Get the pId for the given position name
    cursor.execute("SELECT pId FROM position WHERE positionName = %s", (position,))
    position_id = cursor.fetchone()
    if not position_id:
        cursor.close()
        connection.close()
        return jsonify({"success": False, "message": "Invalid position"}), 400

    position_id = position_id[0]

    query = """
    UPDATE user
    SET fullName = %s, birthday = %s, email = %s, phoneNo = %s, pId = %s
    WHERE username = %s
    """
    print("This is the updated function....")
    print(fullName, birthday, email, phone, position_id, username)

    cursor.execute(query, (fullName, birthday, email, phone, position_id, username))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"success": True, "message": "User profile updated successfully"})


@userProfile_bp.route('/resetPassword', methods=['POST'])
def reset_password():
    data = request.json
    if not data:
        return jsonify({"success": False, "message": "Invalid request"}), 400

    username = data.get('username')
    encrypted_current_password = data.get('currentPassword')
    encrypted_new_password = data.get('newPassword')
    current_password_iv = data.get('currentPasswordIv')
    new_password_iv = data.get('newPasswordIv')

    if not (username and encrypted_current_password and encrypted_new_password and current_password_iv and new_password_iv):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    try:
        current_password = decrypt(encrypted_current_password, current_password_iv)
        new_password = decrypt(encrypted_new_password, new_password_iv)

        print(current_password)
        print(new_password)
    except Exception as e:
        return jsonify({"success": False, "message": "Decryption failed"}), 400

    connection = get_database_connection()
    cursor = connection.cursor()

    query = "SELECT password FROM User WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user and verify_password(user[0], current_password):
        hashed_new_password = hash_password(new_password)
        update_query = "UPDATE User SET password = %s WHERE username = %s"
        cursor.execute(update_query, (hashed_new_password, username))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"success": True, "message": "Password reset successfully"})
    else:
        cursor.close()
        connection.close()
        return jsonify({"success": False, "message": "Current password is incorrect"}), 401
