from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash
from functools import wraps
from src.models import db
from src.models.user import User
from src.models.campaign import Campaign
from src.models.audit_log import AuditLog
from src.models.link import Link
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

def get_current_user():
    """Get current user from token or session"""
    # Try token first
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        user = User.verify_token(token)
        if user:
            return user
    
    # Fall back to session
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    
    return None

def admin_required(f):
    """Decorator to require admin or main_admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        if user.role not in ['admin', 'main_admin']:
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(user, *args, **kwargs)
    return decorated_function

def main_admin_required(f):
    """Decorator to require main_admin role only"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        if user.role != 'main_admin':
            return jsonify({'error': 'Main admin access required'}), 403
        
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
@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users(current_user):
    """Get all users (Main Admin: all users, Admin: members only)"""
    if current_user.role == 'main_admin':
        users = User.query.all()
    else:
        users = User.query.filter_by(role='member').all()
    
    return jsonify([user.to_dict(include_sensitive=True) for user in users])

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(current_user, user_id):
    """Get specific user details"""
    user = User.query.get_or_404(user_id)
    
    # Admin can only view members
    if current_user.role == 'admin' and user.role != 'member':
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify(user.to_dict(include_sensitive=True))

@admin_bp.route('/users', methods=['POST'])
@admin_required
def create_user(current_user):
    """Create new user (Main Admin: any role, Admin: members only)"""
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check role permissions
    role = data.get('role', 'member')
    if current_user.role == 'admin' and role != 'member':
        return jsonify({'error': 'Admin can only create members'}), 403
    
    # Check if username/email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create user
    user = User(
        username=data['username'],
        email=data['email'],
        role=role,
        is_active=data.get('is_active', True),
        is_verified=data.get('is_verified', False),
        plan_type=data.get('plan_type', 'free')
    )
    user.set_password(data['password'])
    
    if 'subscription_expiry' in data:
        user.subscription_expiry = datetime.fromisoformat(data['subscription_expiry'])
    
    db.session.add(user)
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Created user {user.username}", user.id, 'user')
    
    return jsonify(user.to_dict()), 201

@admin_bp.route('/users/<int:user_id>', methods=['PATCH'])
@admin_required
def update_user(current_user, user_id):
    """Update user details"""
    user = User.query.get_or_404(user_id)
    
    # Admin can only edit members
    if current_user.role == 'admin' and user.role != 'member':
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    
    # Update allowed fields
    if 'email' in data:
        user.email = data['email']
    if 'is_active' in data:
        user.is_active = data['is_active']
    if 'is_verified' in data:
        user.is_verified = data['is_verified']
    if 'plan_type' in data:
        user.plan_type = data['plan_type']
    if 'subscription_expiry' in data:
        user.subscription_expiry = datetime.fromisoformat(data['subscription_expiry']) if data['subscription_expiry'] else None
    
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Updated user {user.username}", user.id, 'user')
    
    return jsonify(user.to_dict())

@admin_bp.route('/users/<int:user_id>/role', methods=['PATCH'])
@main_admin_required
def update_user_role(current_user, user_id):
    """Update user role (Main Admin only)"""
    user = User.query.get_or_404(user_id)
    
    # Cannot modify main admin
    if user.role == 'main_admin':
        return jsonify({'error': 'Cannot modify main admin'}), 403
    
    data = request.get_json()
    new_role = data.get('role')
    
    if new_role not in ['admin', 'member']:
        return jsonify({'error': 'Invalid role'}), 400
    
    old_role = user.role
    user.role = new_role
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Changed user {user.username} role from {old_role} to {new_role}", user.id, 'user')
    
    return jsonify(user.to_dict())

@admin_bp.route('/users/<int:user_id>/suspend', methods=['PATCH'])
@admin_required
def suspend_user(current_user, user_id):
    """Suspend/unsuspend user"""
    user = User.query.get_or_404(user_id)
    
    # Cannot suspend main admin
    if user.role == 'main_admin':
        return jsonify({'error': 'Cannot suspend main admin'}), 403
    
    # Admin can only suspend members
    if current_user.role == 'admin' and user.role != 'member':
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    suspend = data.get('suspend', True)
    
    user.is_active = not suspend
    db.session.commit()
    
    action = "Suspended" if suspend else "Unsuspended"
    log_admin_action(current_user.id, f"{action} user {user.username}", user.id, 'user')
    
    return jsonify(user.to_dict())

@admin_bp.route('/users/<int:user_id>/approve', methods=['POST'])
@admin_required
def approve_user(current_user, user_id):
    """Approve pending user"""
    user = User.query.get_or_404(user_id)
    
    # Admin can only approve members
    if current_user.role == 'admin' and user.role != 'member':
        return jsonify({'error': 'Access denied'}), 403
    
    user.status = 'active'
    user.is_verified = True
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Approved user {user.username}", user.id, 'user')
    
    return jsonify(user.to_dict())

@admin_bp.route('/users/<int:user_id>/suspend', methods=['POST'])
@admin_required
def suspend_user_action(current_user, user_id):
    """Suspend user (POST endpoint for admin panel)"""
    user = User.query.get_or_404(user_id)
    
    # Cannot suspend main admin
    if user.role == 'main_admin':
        return jsonify({'error': 'Cannot suspend main admin'}), 403
    
    # Admin can only suspend members
    if current_user.role == 'admin' and user.role != 'member':
        return jsonify({'error': 'Access denied'}), 403
    
    user.status = 'suspended'
    user.is_active = False
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Suspended user {user.username}", user.id, 'user')
    
    return jsonify(user.to_dict())

@admin_bp.route('/users/<int:user_id>/view', methods=['POST'])
@admin_required
def view_user_action(current_user, user_id):
    """View user details (POST endpoint for admin panel)"""
    user = User.query.get_or_404(user_id)
    
    # Admin can only view members
    if current_user.role == 'admin' and user.role != 'member':
        return jsonify({'error': 'Access denied'}), 403
    
    # Log action
    log_admin_action(current_user.id, f"Viewed user {user.username}", user.id, 'user')
    
    return jsonify(user.to_dict(include_sensitive=True))

# Campaign Management Endpoints
@admin_bp.route('/campaigns', methods=['GET'])
@admin_required
def get_campaigns(current_user):
    """Get all campaigns"""
    campaigns = Campaign.query.all()
    return jsonify([campaign.to_dict() for campaign in campaigns])

@admin_bp.route('/campaigns/<int:campaign_id>', methods=['GET'])
@admin_required
def get_campaign(current_user, campaign_id):
    """Get specific campaign details"""
    campaign = Campaign.query.get_or_404(campaign_id)
    return jsonify(campaign.to_dict())

@admin_bp.route('/campaigns', methods=['POST'])
@admin_required
def create_campaign(current_user):
    """Create new campaign"""
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Campaign name is required'}), 400
    
    campaign = Campaign(
        name=data['name'],
        description=data.get('description', ''),
        owner_id=current_user.id,
        status=data.get('status', 'active')
    )
    
    db.session.add(campaign)
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Created campaign {campaign.name}", campaign.id, 'campaign')
    
    return jsonify(campaign.to_dict()), 201

@admin_bp.route('/campaigns/<int:campaign_id>', methods=['PATCH'])
@admin_required
def update_campaign(current_user, campaign_id):
    """Update campaign details"""
    campaign = Campaign.query.get_or_404(campaign_id)
    data = request.get_json()
    
    if 'name' in data:
        campaign.name = data['name']
    if 'description' in data:
        campaign.description = data['description']
    if 'status' in data:
        campaign.status = data['status']
    
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Updated campaign {campaign.name}", campaign.id, 'campaign')
    
    return jsonify(campaign.to_dict())

@admin_bp.route('/campaigns/<int:campaign_id>', methods=['DELETE'])
@admin_required
def delete_campaign(current_user, campaign_id):
    """Delete campaign"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    campaign_name = campaign.name
    db.session.delete(campaign)
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Deleted campaign {campaign_name}", campaign_id, 'campaign')
    
    return jsonify({'message': 'Campaign deleted successfully'})

@admin_bp.route('/campaigns/<int:campaign_id>/links', methods=['GET'])
@admin_required
def get_campaign_links(current_user, campaign_id):
    """Get all links for a specific campaign"""
    campaign = Campaign.query.get_or_404(campaign_id)
    links = Link.query.filter_by(campaign_id=campaign_id).all()
    return jsonify([link.to_dict() for link in links])

# Analytics Endpoints
@admin_bp.route('/analytics/users', methods=['GET'])
@admin_required
def get_user_analytics(current_user):
    """Get system-wide user analytics"""
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    suspended_users = User.query.filter_by(is_active=False).count()
    verified_users = User.query.filter_by(is_verified=True).count()
    
    # Users by role
    main_admins = User.query.filter_by(role='main_admin').count()
    admins = User.query.filter_by(role='admin').count()
    members = User.query.filter_by(role='member').count()
    
    # Users by plan
    free_users = User.query.filter_by(plan_type='free').count()
    pro_users = User.query.filter_by(plan_type='pro').count()
    enterprise_users = User.query.filter_by(plan_type='enterprise').count()
    
    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'suspended_users': suspended_users,
        'verified_users': verified_users,
        'users_by_role': {
            'main_admin': main_admins,
            'admin': admins,
            'member': members
        },
        'users_by_plan': {
            'free': free_users,
            'pro': pro_users,
            'enterprise': enterprise_users
        }
    })

@admin_bp.route('/analytics/campaigns', methods=['GET'])
@admin_required
def get_campaign_analytics(current_user):
    """Get system-wide campaign analytics"""
    total_campaigns = Campaign.query.count()
    active_campaigns = Campaign.query.filter_by(status='active').count()
    paused_campaigns = Campaign.query.filter_by(status='paused').count()
    completed_campaigns = Campaign.query.filter_by(status='completed').count()
    
    # Total links across all campaigns
    total_links = Link.query.count()
    
    return jsonify({
        'total_campaigns': total_campaigns,
        'active_campaigns': active_campaigns,
        'paused_campaigns': paused_campaigns,
        'completed_campaigns': completed_campaigns,
        'total_links': total_links
    })

@admin_bp.route('/users/<int:user_id>/change-password', methods=['POST'])
@admin_required
def change_user_password(current_user, user_id):
    """Change user password (admin action)"""
    user = User.query.get_or_404(user_id)
    
    # Admin can only change member passwords, main admin can change anyone's except their own username
    if current_user.role == 'admin' and user.role != 'member':
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    if not data or 'new_password' not in data:
        return jsonify({'error': 'New password is required'}), 400
    
    new_password = data['new_password']
    if len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400
    
    # Update password
    user.password_hash = generate_password_hash(new_password)
    user.updated_at = datetime.utcnow()
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Changed password for user {user.username}", user.id, 'user')
    
    return jsonify({'message': f'Password changed successfully for user {user.username}'})

@admin_bp.route('/users/<int:user_id>/extend', methods=['POST'])
@admin_required
def extend_user_subscription(current_user, user_id):
    """Extend user subscription (POST endpoint for admin panel)"""
    user = User.query.get_or_404(user_id)
    
    # Admin can only extend members
    if current_user.role == 'admin' and user.role != 'member':
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json() or {}
    days_to_extend = data.get('days', 30)  # Default 30 days
    
    # Extend subscription
    if user.subscription_end:
        user.subscription_end = user.subscription_end + timedelta(days=days_to_extend)
    else:
        user.subscription_end = datetime.utcnow() + timedelta(days=days_to_extend)
    
    # Update status if expired
    if user.status == 'expired':
        user.status = 'active'
    
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Extended user {user.username} subscription by {days_to_extend} days", user.id, 'user')
    
    return jsonify(user.to_dict())

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user_action(current_user, user_id):
    """Delete user (POST endpoint for admin panel)"""
    user = User.query.get_or_404(user_id)
    
    # Cannot delete main admin
    if user.role == 'main_admin':
        return jsonify({'error': 'Cannot delete main admin'}), 403
    
    # Admin can only delete members
    if current_user.role == 'admin' and user.role != 'member':
        return jsonify({'error': 'Access denied'}), 403
    
    username = user.username
    
    # Delete user
    db.session.delete(user)
    db.session.commit()
    
    # Log action
    log_admin_action(current_user.id, f"Deleted user {username}", user_id, 'user')
    
    return jsonify({'message': f'User {username} deleted successfully'})

# Audit Logs Endpoints
@admin_bp.route('/audit-logs', methods=['GET'])
@admin_required
def get_audit_logs(current_user):
    """Get audit logs"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'logs': [log.to_dict() for log in logs.items],
        'total': logs.total,
        'pages': logs.pages,
        'current_page': page
    })

@admin_bp.route('/audit-logs/<int:log_id>', methods=['GET'])
@admin_required
def get_audit_log(current_user, log_id):
    """Get specific audit log"""
    log = AuditLog.query.get_or_404(log_id)
    return jsonify(log.to_dict())

<<<<<<< HEAD
@admin_bp.route('/audit-logs/export', methods=['GET'])
@admin_required
def export_audit_logs(current_user):
    """Export audit logs as CSV"""
    import csv
    from io import StringIO
    from flask import make_response

    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).all()

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['ID', 'Actor ID', 'Action', 'Target Type', 'Target ID', 'IP Address', 'Created At'])

    for log in logs:
        writer.writerow([log.id, log.actor_id, log.action, log.target_type, log.target_id, log.ip_address, log.created_at])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=audit_logs.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@admin_bp.route('/system/delete-all', methods=['POST'])
@main_admin_required
def delete_all_system_data(current_user):
    """Delete all system data (DANGEROUS - Main Admin only)"""
    try:
        confirm = request.get_json().get('confirm')
        if confirm != 'DELETE_ALL_DATA':
            return jsonify({'error': 'Confirmation text required'}), 400

        # Delete in correct order to respect foreign keys
        TrackingEvent.query.delete()
        Link.query.delete()
        Campaign.query.filter(Campaign.owner_id != current_user.id).delete()
        AuditLog.query.delete()
        User.query.filter(User.id != current_user.id, User.role != 'main_admin').delete()

        db.session.commit()

        log_admin_action(current_user.id, 'System reset - All data deleted', None, 'system')

        return jsonify({'message': 'All system data deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/dashboard/stats', methods=['GET'])
@admin_required
def get_dashboard_stats(current_user):
    """Get comprehensive dashboard statistics"""
    from sqlalchemy import func
    from datetime import datetime, timedelta

    try:
        # User statistics
        total_users = User.query.count()
        active_users = User.query.filter_by(status='active').count()
        pending_users = User.query.filter_by(status='pending').count()
        suspended_users = User.query.filter_by(status='suspended').count()

        # Campaign statistics
        total_campaigns = Campaign.query.count()
        active_campaigns = Campaign.query.filter_by(status='active').count()

        # Link statistics
        total_links = Link.query.count()
        active_links = Link.query.filter_by(status='active').count()

        # Event statistics
        total_events = TrackingEvent.query.count()
        today = datetime.utcnow().date()
        today_events = TrackingEvent.query.filter(func.date(TrackingEvent.timestamp) == today).count()

        # Get recent activity
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        recent_events = TrackingEvent.query.order_by(TrackingEvent.timestamp.desc()).limit(10).all()

        return jsonify({
            'users': {
                'total': total_users,
                'active': active_users,
                'pending': pending_users,
                'suspended': suspended_users
            },
            'campaigns': {
                'total': total_campaigns,
                'active': active_campaigns
            },
            'links': {
                'total': total_links,
                'active': active_links
            },
            'events': {
                'total': total_events,
                'today': today_events
            },
            'recent_users': [u.to_dict() for u in recent_users],
            'recent_events': [e.to_dict() for e in recent_events]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

=======
>>>>>>> 00392b0 (Initial commit of unified Brain Link Tracker project with integrated admin panel fixes)
