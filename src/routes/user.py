from flask import Blueprint, request, jsonify, session
from src.models.user import User, db
from functools import wraps
from werkzeug.utils import secure_filename
import re
import os
import base64
from datetime import datetime

user_bp = Blueprint("user", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function

def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def sanitize_input(text):
    if not text:
        return ""
    return text.strip()

@user_bp.route("/user/profile", methods=["GET"])
@login_required
def get_profile():
    """Get user profile"""
    try:
        user_id = session.get("user_id")
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/user/profile", methods=["PATCH"])
@login_required
def update_profile():
    """Update user profile"""
    try:
        user_id = session.get("user_id")
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()

        if "email" in data:
            existing = User.query.filter_by(email=data["email"]).first()
            if existing and existing.id != user.id:
                return jsonify({"error": "Email already in use"}), 400
            user.email = data["email"]

        if "settings" in data:
            user.settings = data["settings"]

        db.session.commit()

        return jsonify(user.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@user_bp.route("/user/password", methods=["PATCH"])
@login_required
def change_password():
    """Change user password"""
    try:
        user_id = session.get("user_id")
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        if not current_password or not new_password:
            return jsonify({"error": "Current and new password required"}), 400

        if not user.check_password(current_password):
            return jsonify({"error": "Current password is incorrect"}), 400

        if len(new_password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400

        user.set_password(new_password)
        db.session.commit()

        return jsonify({"message": "Password updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@user_bp.route("/user/change-password", methods=["POST"])
@login_required
def change_password_new():
    """Change user password (new endpoint for profile)"""
    try:
        user_id = session.get("user_id")
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        if not current_password or not new_password:
            return jsonify({"error": "Current and new password required"}), 400

        if not user.check_password(current_password):
            return jsonify({"error": "Current password is incorrect"}), 400

        if len(new_password) < 8:
            return jsonify({"error": "Password must be at least 8 characters"}), 400

        user.set_password(new_password)
        db.session.commit()

        return jsonify({"success": True, "message": "Password changed successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@user_bp.route("/user/profile", methods=["PUT"])
@login_required  
def update_profile_complete():
    """Update user profile with avatar support"""
    try:
        user_id = session.get("user_id")
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Handle both JSON and FormData
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle file upload
            username = request.form.get('username')
            email = request.form.get('email')
            avatar = request.files.get('avatar')
            
            if username:
                user.username = sanitize_input(username)
            
            if email:
                if not validate_email(email):
                    return jsonify({"error": "Invalid email format"}), 400
                
                existing = User.query.filter_by(email=email).first()
                if existing and existing.id != user.id:
                    return jsonify({"error": "Email already in use"}), 400
                user.email = email
            
            if avatar:
                # Save avatar file
                filename = secure_filename(avatar.filename)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                avatar_filename = f"avatar_{user_id}_{timestamp}_{filename}"
                
                # Create uploads directory if it doesn't exist
                upload_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads', 'avatars')
                os.makedirs(upload_dir, exist_ok=True)
                
                avatar_path = os.path.join(upload_dir, avatar_filename)
                avatar.save(avatar_path)
                
                # Store relative path
                user.avatar_url = f"/uploads/avatars/{avatar_filename}"
        else:
            # Handle JSON
            data = request.get_json()
            
            if 'username' in data:
                user.username = sanitize_input(data['username'])
            
            if 'email' in data:
                if not validate_email(data['email']):
                    return jsonify({"error": "Invalid email format"}), 400
                
                existing = User.query.filter_by(email=data['email']).first()
                if existing and existing.id != user.id:
                    return jsonify({"error": "Email already in use"}), 400
                user.email = data['email']

        db.session.commit()
        return jsonify(user.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error updating profile: {e}")
        return jsonify({"error": str(e)}), 500

# Admin-related user management routes (from the 00392b0 version)
# These routes should ideally be in an admin-specific blueprint and protected by admin role checks.
# For now, they are included here, but note that they lack authentication/authorization.

@user_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(username=data["username"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return "", 204

