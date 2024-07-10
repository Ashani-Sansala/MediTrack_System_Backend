from flask import Blueprint, jsonify, request
from utils.dbConn import get_database_connection
from utils.encryption import decrypt, verify_password, hash_password
from utils.firebase_init import get_storage_bucket
import os
import uuid
from mysql.connector import Error

# Blueprint for user profile functionality
userProfile_bp = Blueprint('userProfile', __name__)

# Route to get user profile details
@userProfile_bp.route('/getUserProfile', methods=['GET', 'POST'])
def get_user_profile():
    data = request.json
    username = str(data.get('username'))
    
    # Check if username is provided
    if not username:
        return jsonify({"success": False, "message": "User not logged in"}), 401
    
    connection = get_database_connection()
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.callproc('GetUserProfile', (username,))
            for result in cursor.stored_results():
                user = result.fetchone()

        # Return user details if found
        if user:
            return jsonify({"success": True, "userDetails": user})
        else:
            return jsonify({"success": False, "message": "User not found"}), 404
    except Error as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        connection.close()

# Route to update user profile details
@userProfile_bp.route('/updateUserProfile', methods=['POST'])
def update_user_profile():
    try:
        encrypted_username = request.form['username']

        # Check if username is provided
        if not encrypted_username:
            return jsonify({"success": False, "message": "User not logged in"}), 401

        required_fields = ['fullName', 'birthday', 'email', 'phoneNo', 'positionName', 'usernameIv', 'emailIv', 'phoneNoIv']
        if not all(request.form[field] for field in required_fields):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        try:
            data = request.form
            # Decrypt sensitive information
            username = decrypt(encrypted_username, data['usernameIv'])
            email = decrypt(data['email'], data['emailIv'])
            phoneNo = decrypt(data['phoneNo'], data['phoneNoIv'])
        except Exception as e:
            return jsonify({"success": False, "message": "Try again!"}), 400

        # Handle avatar upload if provided
        avatar_url = None
        if 'avatar' in request.files:
            avatar_file = request.files['avatar']
            if avatar_file.filename != '':
                file_extension = os.path.splitext(avatar_file.filename)[1]
                unique_filename = f"{uuid.uuid4()}{file_extension}"
                bucket = get_storage_bucket()
                blob = bucket.blob(f"avatars/{unique_filename}")
                blob.upload_from_string(
                    avatar_file.read(),
                    content_type=avatar_file.content_type
                )
                blob.make_public()
                avatar_url = blob.public_url

        connection = get_database_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.callproc('UpdateUserProfile', (
                    username,
                    request.form['fullName'],
                    request.form['birthday'],
                    email,
                    phoneNo,
                    request.form['positionName'],
                    avatar_url
                ))
                for result in cursor.stored_results():
                    updated_user = result.fetchone()

            connection.commit()

            # Return updated user details if successful
            if updated_user:
                return jsonify({
                    "success": True, 
                    "message": "User profile updated successfully",
                    "fullName": updated_user['fullName'],
                    "avatarUrl": updated_user['avatarUrl']
                }), 200
            else:
                return jsonify({"success": False, "message": "Failed to update user profile"}), 500
        except Error as e:
            print(str(e))
            connection.rollback()
            return jsonify({"success": False, "message": str(e)}), 500
        finally:
            connection.close()
    except Exception as e:
        print(str(e))
        return jsonify({"success": False, "message": str(e)}), 500

# Route to reset user password
@userProfile_bp.route('/resetPassword', methods=['POST'])
def reset_password():
    data = request.json
    if not data:
        return jsonify({"success": False, "message": "Invalid request"}), 400

    required_fields = ['username', 'currentPassword', 'newPassword', 'currentPasswordIv', 'newPasswordIv']
    if not all(field in data for field in required_fields):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    try:
        # Decrypt current and new passwords
        current_password = decrypt(data['currentPassword'], data['currentPasswordIv'])
        new_password = decrypt(data['newPassword'], data['newPasswordIv'])
    except Exception as e:
        return jsonify({"success": False, "message": "Decryption failed"}), 400

    connection = get_database_connection()
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT password FROM user WHERE username = %s", (data['username'],))
            user = cursor.fetchone()

            # Verify current password and update with new password if correct
            if user and verify_password(user['password'], current_password):
                hashed_new_password = hash_password(new_password)
                cursor.callproc('ResetPassword', (data['username'], hashed_new_password))
                connection.commit()
                return jsonify({"success": True, "message": "Password reset successfully"})
            else:
                return jsonify({"success": False, "message": "Current password is incorrect"}), 401
    except Error as e:
        connection.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        connection.close()
