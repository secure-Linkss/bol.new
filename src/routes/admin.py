from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash
from functools import wraps
from src.models import db
from src.models.user import User
from src.models.campaign import Campaign
from src.models.audit_log import AuditLog
from src.models.link import Link
from datetime import datetime, timedelta

admin_bp = Blueprint("admin", __name__)

def get_current_user():
    """Get current user from token or session"""
    # Try token first
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        user = User.verify_token(token)
        if user:
            return user
    
    # Fall back to session
    if "user_id" in session:
        return User.query.get(session["user_id"])
    
    return None

def admin_required(f):
    """Decorator to require admin or main_admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        
        if user.role not in ["admin", "main_admin"]:
            return jsonify({"error": "Admin access required"}), 403
        
        return f(user, *args, **kwargs)
    return decorated_function

def main_admin_required(f):
    """Decorator to require main_admin role only"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        
        if user.role != "main_admin":
            return jsonify({"error": "Main admin access required"}), 403
        
        return f(user, *args, **kwargs)
    return decorated_function

def log_admin_action(actor_id, action, target_id=None, target_type=None):
    """Log admin actions to audit_logs"""
    audit_log = AuditLog(
        actor_id=actor_id,
        action=action,
        target_id=target_id,
        target_type=target_type
    )
    db.session.add(audit_log)
    db.session.commit()

# User Management Endpoints
@admin_bp.route("/api/admin/users", methods=["GET"])
@admin_required
def get_users(current_user):
    """Get all users (Main Admin: all users, Admin: members only)"""
    if current_user.role == "main_admin":
        users = User.query.all()
    else:
        users = User.query.filter_by(role="member").all()
    
    return jsonify([user.to_dict(include_sensitive=True) for user in users])

@admin_bp.route("/api/admin/users/<int:user_id>", methods=["GET"])
@admin_required
def get_user(current_user, user_id):
    """Get specific user details"""
    user = User.query.get_or_404(user_id)
    
    # Admin can only view members
    if current_user.role == "admin" and user.role != "member":
        return jsonify({"error": "Access denied"}), 403
    
    return jsonify(user.to_dict(include_sensitive=True))

@admin_bp.route("/api/admin/users", methods=["POST"])
@admin_required
def create_user(current_user):
    """Create new user (Main Admin: any role, Admin: members only)"""
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ["username", "email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Check role permissions
    role = data.get("role", "member")
    if current_user.role == "admin" and role != "member":
        return jsonify({"error": "Admin can only create members"}), 403
    
    # Check if username/email already exists
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400
    
    # Create user
    user = User(
        username=data["username"],
        email=data["email"],
        role=role,
        is_active=data.get("is_active", True),
        is_verified=data.get("is_verified", False),
        plan_type=data.get("plan_type", "free")
    )
    user.set_password(data["password"])
    
    if "subscription_expiry" in data:
        user.subscription_expiry = datetime.fromisoformat(data["subscription_expiry"]) if data["subscription_expiry"] else None
    
    db.session.add(user)
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Created user {user.username}", user.id, "user")
    
    return jsonify(user.to_dict()), 201

@admin_bp.route("/api/admin/users/<int:user_id>", methods=["PATCH"])
@admin_required
def update_user(current_user, user_id):
    """Update user details"""
    user = User.query.get_or_404(user_id)
    
    # Admin can only edit members
    if current_user.role == "admin" and user.role != "member":
        return jsonify({"error": "Access denied"}), 403
    
    data = request.get_json()
    
    # Update allowed fields
    if "email" in data:
        user.email = data["email"]
    if "is_active" in data:
        user.is_active = data["is_active"]
    if "is_verified" in data:
        user.is_verified = data["is_verified"]
    if "plan_type" in data:
        user.plan_type = data["plan_type"]
    if "subscription_expiry" in data:
        user.subscription_expiry = datetime.fromisoformat(data["subscription_expiry"]) if data["subscription_expiry"] else None
    
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Updated user {user.username}", user.id, "user")
    
    return jsonify(user.to_dict())

@admin_bp.route("/api/admin/users/<int:user_id>/role", methods=["PATCH"])
@main_admin_required
def update_user_role(current_user, user_id):
    """Update user role (Main Admin only)"""
    user = User.query.get_or_404(user_id)
    
    # Cannot modify main admin
    if user.role == "main_admin":
        return jsonify({"error": "Cannot modify main admin"}), 403
    
    data = request.get_json()
    new_role = data.get("role")
    
    if new_role not in ["admin", "member"]:
        return jsonify({"error": "Invalid role"}), 400
    
    old_role = user.role
    user.role = new_role
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Changed user {user.username} role from {old_role} to {new_role}", user.id, "user")
    
    return jsonify(user.to_dict())

@admin_bp.route("/api/admin/users/<int:user_id>/suspend", methods=["PATCH"])
@admin_required
def suspend_user(current_user, user_id):
    """Suspend/unsuspend user"""
    user = User.query.get_or_404(user_id)
    
    # Cannot suspend main admin
    if user.role == "main_admin":
        return jsonify({"error": "Cannot suspend main admin"}), 403
    
    # Admin can only suspend members
    if current_user.role == "admin" and user.role != "member":
        return jsonify({"error": "Access denied"}), 403
    
    data = request.get_json()
    suspend = data.get("suspend", True)
    
    user.is_active = not suspend
    db.session.commit()
    
    action = "Suspended" if suspend else "Unsuspended"
    log_admin_action(current_user.id, f"{action} user {user.username}", user.id, "user")
    
    return jsonify(user.to_dict())

@admin_bp.route("/api/admin/users/<int:user_id>/approve", methods=["POST"])
@admin_required
def approve_user(current_user, user_id):
    """Approve pending user"""
    user = User.query.get_or_404(user_id)
    
    # Admin can only approve members
    if current_user.role == "admin" and user.role != "member":
        return jsonify({"error": "Access denied"}), 403
    
    user.status = "active"
    user.is_active = True # Ensure is_active is also set
    user.is_verified = True
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Approved user {user.username}", user.id, "user")
    
    return jsonify(user.to_dict())

@admin_bp.route("/api/admin/users/<int:user_id>/change-password", methods=["POST"])
@admin_required
def change_user_password(current_user, user_id):
    """Change user password (admin action)"""
    user = User.query.get_or_404(user_id)
    
    # Admin can only change member passwords, main admin can change anyone's except their own username
    if current_user.role == "admin" and user.role != "member":
        return jsonify({"error": "Access denied"}), 403
    
    data = request.get_json()
    if not data or "new_password" not in data:
        return jsonify({"error": "New password is required"}), 400
    
    new_password = data["new_password"]
    if len(new_password) < 6:
        return jsonify({"error": "Password must be at least 6 characters long"}), 400
    
    # Update password
    user.set_password(new_password) # Use set_password method
    user.updated_at = datetime.utcnow()
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Changed password for user {user.username}", user.id, "user")
    
    return jsonify({"message": f"Password changed successfully for user {user.username}"})

@admin_bp.route("/api/admin/users/<int:user_id>/extend", methods=["POST"])
@admin_required
def extend_user_subscription(current_user, user_id):
    """Extend user subscription (POST endpoint for admin panel)"""
    user = User.query.get_or_404(user_id)
    
    # Admin can only extend members
    if current_user.role == "admin" and user.role != "member":
        return jsonify({"error": "Access denied"}), 403
    
    data = request.get_json() or {}
    days_to_extend = data.get("days", 30)  # Default 30 days
    
    # Extend subscription
    if user.subscription_expiry:
        user.subscription_expiry = user.subscription_expiry + timedelta(days=days_to_extend)
    else:
        user.subscription_expiry = datetime.utcnow() + timedelta(days=days_to_extend)
    
    # Update status if expired
    if user.status == "expired":
        user.status = "active"
    
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Extended user {user.username} subscription by {days_to_extend} days", user.id, "user")
    
    return jsonify(user.to_dict())

@admin_bp.route("/api/admin/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete_user_action(current_user, user_id):
    """Delete user (POST endpoint for admin panel)"""
    user = User.query.get_or_404(user_id)
    
    # Cannot delete main admin
    if user.role == "main_admin":
        return jsonify({"error": "Cannot delete main admin"}), 403
    
    # Admin can only delete members
    if current_user.role == "admin" and user.role != "member":
        return jsonify({"error": "Access denied"}), 403
    
    user_username = user.username
    db.session.delete(user)
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Deleted user {user_username}", user_id, "user")
    
    return jsonify({"message": f"User {user_username} deleted successfully"})


# Campaign Management Endpoints
@admin_bp.route("/api/admin/campaigns", methods=["GET"])
@admin_required
def get_campaigns(current_user):
    """Get all campaigns"""
    campaigns = Campaign.query.all()
    return jsonify([campaign.to_dict() for campaign in campaigns])

@admin_bp.route("/api/admin/campaigns/<int:campaign_id>", methods=["GET"])
@admin_required
def get_campaign(current_user, campaign_id):
    """Get specific campaign details"""
    campaign = Campaign.query.get_or_404(campaign_id)
    return jsonify(campaign.to_dict())

@admin_bp.route("/api/admin/campaigns", methods=["POST"])
@admin_required
def create_campaign(current_user):
    """Create new campaign"""
    data = request.get_json()
    
    if not data.get("name"):
        return jsonify({"error": "Campaign name is required"}), 400
    
    campaign = Campaign(
        name=data["name"],
        description=data.get("description", ""),
        owner_id=current_user.id,
        status=data.get("status", "active")
    )
    
    db.session.add(campaign)
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Created campaign {campaign.name}", campaign.id, "campaign")
    
    return jsonify(campaign.to_dict()), 201

@admin_bp.route("/api/admin/campaigns/<int:campaign_id>", methods=["PATCH"])
@admin_required
def update_campaign(current_user, campaign_id):
    """Update campaign details"""
    campaign = Campaign.query.get_or_404(campaign_id)
    data = request.get_json()
    
    if "name" in data:
        campaign.name = data["name"]
    if "description" in data:
        campaign.description = data["description"]
    if "status" in data:
        campaign.status = data["status"]
    
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Updated campaign {campaign.name}", campaign.id, "campaign")
    
    return jsonify(campaign.to_dict())

@admin_bp.route("/api/admin/campaigns/<int:campaign_id>", methods=["DELETE"])
@admin_required
def delete_campaign(current_user, campaign_id):
    """Delete campaign"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    campaign_name = campaign.name
    db.session.delete(campaign)
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Deleted campaign {campaign_name}", campaign_id, "campaign")
    
    return jsonify({"message": "Campaign deleted successfully"})


@admin_bp.route("/api/admin/campaigns/<int:campaign_id>/links", methods=["GET"])
@admin_required
def get_campaign_links(current_user, campaign_id):
    """Get all links for a specific campaign"""
    campaign = Campaign.query.get_or_404(campaign_id)
    links = Link.query.filter_by(campaign_id=campaign_id).all()
    return jsonify([link.to_dict() for link in links])

# Analytics Endpoints
@admin_bp.route("/api/admin/analytics/users", methods=["GET"])
@admin_required
def get_user_analytics(current_user):
    """Get system-wide user analytics"""
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    suspended_users = User.query.filter_by(is_active=False).count()
    verified_users = User.query.filter_by(is_verified=True).count()
    
    # Users by role
    main_admins = User.query.filter_by(role="main_admin").count()
    admins = User.query.filter_by(role="admin").count()
    members = User.query.filter_by(role="member").count()
    
    # Users by plan
    free_users = User.query.filter_by(plan_type="free").count()
    pro_users = User.query.filter_by(plan_type="pro").count()
    enterprise_users = User.query.filter_by(plan_type="enterprise").count()
    
    return jsonify({
        "total_users": total_users,
        "active_users": active_users,
        "suspended_users": suspended_users,
        "verified_users": verified_users,
        "users_by_role": {
            "main_admin": main_admins,
            "admin": admins,
            "member": members
        },
        "users_by_plan": {
            "free": free_users,
            "pro": pro_users,
            "enterprise": enterprise_users
        }
    })

@admin_bp.route("/api/admin/analytics/campaigns", methods=["GET"])
@admin_required
def get_campaign_analytics(current_user):
    """Get system-wide campaign analytics"""
    total_campaigns = Campaign.query.count()
    active_campaigns = Campaign.query.filter_by(status="active").count()
    paused_campaigns = Campaign.query.filter_by(status="paused").count()
    completed_campaigns = Campaign.query.filter_by(status="completed").count()
    
    # Total links across all campaigns
    total_links = Link.query.count()
    
    return jsonify({
        "total_campaigns": total_campaigns,
        "active_campaigns": active_campaigns,
        "paused_campaigns": paused_campaigns,
        "completed_campaigns": completed_campaigns,
        "total_links": total_links
    })

@admin_bp.route("/api/admin/audit-logs", methods=["GET"])
@main_admin_required
def get_audit_logs(current_user):
    """Get all audit logs (Main Admin only)"""
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return jsonify([log.to_dict() for log in logs])

