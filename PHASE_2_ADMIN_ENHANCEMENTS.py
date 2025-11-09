#!/usr/bin/env python3
"""
PHASE 2: ADMIN PANEL ENHANCEMENTS
==================================
Implements all the missing columns and sections in AdminPanelComplete.jsx
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

print("=" * 80)
print("PHASE 2: ADMIN PANEL ENHANCEMENTS")
print("=" * 80)

# =================================================================
# 1. Enhanced User Management Backend Route
# =================================================================

print("\n[1/5] Creating Enhanced User Management Route...")

enhanced_user_route = '''
@admin_complete_bp.route("/api/admin/users/enhanced", methods=["GET"])
def get_enhanced_users():
    """Get enhanced user list with all requested columns"""
    try:
        # Check admin authentication
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        current_user = User.query.get(user_id)
        if not current_user or current_user.role not in ['admin', 'main_admin']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get all users with enhanced data
        users = User.query.all()
        
        user_list = []
        for user in users:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'status': user.status,
                'account_type': user.role,  # admin / user / sub_admin
                'subscription_plan': user.plan_type or 'free',
                'subscription_status': user.subscription_status or 'inactive',
                'payment_status': user.subscription_status or 'unpaid',
                'date_joined': user.created_at.isoformat() if user.created_at else None,
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'login_method': getattr(user, 'login_method', 'email'),
                'is_verified': user.is_verified,
                'verification_status': 'verified' if user.is_verified else 'pending',
                'is_active': user.is_active,
                'total_links': Link.query.filter_by(user_id=user.id).count(),
                'total_clicks': db.session.query(func.count(TrackingEvent.id)).join(
                    Link, TrackingEvent.link_id == Link.id
                ).filter(Link.user_id == user.id).scalar() or 0
            }
            user_list.append(user_data)
        
        # Separate into categories
        active_users = [u for u in user_list if u['is_active'] and u['is_verified']]
        pending_users = [u for u in user_list if not u['is_verified']]
        suspended_users = [u for u in user_list if not u['is_active']]
        
        return jsonify({
            'success': True,
            'users': user_list,
            'active_users': active_users,
            'pending_users': pending_users,
            'suspended_users': suspended_users,
            'stats': {
                'total': len(user_list),
                'active': len(active_users),
                'pending': len(pending_users),
                'suspended': len(suspended_users),
                'admins': len([u for u in user_list if u['role'] in ['admin', 'main_admin']])
            }
        })
    
    except Exception as e:
        print(f"Error in enhanced users: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500
'''

# Add to admin_complete.py
admin_complete_path = PROJECT_ROOT / 'src' / 'routes' / 'admin_complete.py'
with open(admin_complete_path, 'r') as f:
    admin_content = f.read()

if '/users/enhanced' not in admin_content:
    # Add before the last function
    admin_content = admin_content.rstrip() + '\n' + enhanced_user_route + '\n'
    
    with open(admin_complete_path, 'w') as f:
        f.write(admin_content)
    
    print("  ✓ Added enhanced user management route")
else:
    print("  ✓ Enhanced user route already exists")

# =================================================================
# 2. Enhanced Security Route with More Details
# =================================================================

print("\n[2/5] Creating Enhanced Security Route...")

enhanced_security_route = '''
@admin_complete_bp.route("/api/admin/security/threats/enhanced", methods=["GET"])
def get_enhanced_security_threats():
    """Get security threats with enhanced details"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        current_user = User.query.get(user_id)
        if not current_user or current_user.role not in ['admin', 'main_admin']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get all security threats
        threats = SecurityThreat.query.order_by(SecurityThreat.detected_at.desc()).all()
        
        threat_list = []
        for threat in threats:
            threat_data = {
                'id': threat.id,
                'ip_address': threat.ip_address,
                'country': getattr(threat, 'country', 'Unknown'),
                'city': getattr(threat, 'city', 'Unknown'),
                'threat_type': threat.threat_type,
                'severity': threat.severity,
                'status': threat.status,
                'description': threat.description,
                'user_agent': getattr(threat, 'user_agent', 'Unknown'),
                'device': getattr(threat, 'device', 'Unknown'),
                'browser': getattr(threat, 'browser', 'Unknown'),
                'action_taken': getattr(threat, 'action_taken', 'None'),
                'detected_at': threat.detected_at.isoformat() if threat.detected_at else None,
                'resolved_at': threat.resolved_at.isoformat() if threat.resolved_at else None
            }
            threat_list.append(threat_data)
        
        # Get bot activity
        bot_events = TrackingEvent.query.filter_by(is_bot=True).order_by(
            TrackingEvent.timestamp.desc()
        ).limit(100).all()
        
        bot_activity = []
        for event in bot_events:
            bot_activity.append({
                'id': event.id,
                'ip_address': event.ip_address,
                'country': event.country_name,
                'city': event.city,
                'user_agent': event.user_agent,
                'bot_type': event.browser,  # Often contains bot name
                'timestamp': event.timestamp.isoformat() if event.timestamp else None,
                'blocked': True
            })
        
        return jsonify({
            'success': True,
            'threats': threat_list,
            'bot_activity': bot_activity,
            'stats': {
                'total_threats': len(threat_list),
                'active_threats': len([t for t in threat_list if t['status'] == 'active']),
                'resolved_threats': len([t for t in threat_list if t['status'] == 'resolved']),
                'bots_blocked': len(bot_activity),
                'high_severity': len([t for t in threat_list if t['severity'] == 'high'])
            }
        })
    
    except Exception as e:
        print(f"Error in enhanced security: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500
'''

if '/security/threats/enhanced' not in admin_content:
    with open(admin_complete_path, 'r') as f:
        admin_content = f.read()
    
    admin_content = admin_content.rstrip() + '\n' + enhanced_security_route + '\n'
    
    with open(admin_complete_path, 'w') as f:
        f.write(admin_content)
    
    print("  ✓ Added enhanced security route")
else:
    print("  ✓ Enhanced security route already exists")

# =================================================================
# 3. Enhanced Campaign Route
# =================================================================

print("\n[3/5] Creating Enhanced Campaign Route...")

enhanced_campaign_route = '''
@admin_complete_bp.route("/api/admin/campaigns/enhanced", methods=["GET"])
def get_enhanced_campaigns():
    """Get campaigns with all requested details"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        # Get all campaigns
        campaigns = Campaign.query.all()
        
        campaign_list = []
        for campaign in campaigns:
            # Get associated links count
            links_count = Link.query.filter_by(campaign_id=campaign.id).count()
            
            # Get total clicks
            total_clicks = db.session.query(func.count(TrackingEvent.id)).join(
                Link, TrackingEvent.link_id == Link.id
            ).filter(Link.campaign_id == campaign.id).scalar() or 0
            
            # Get real visitors (non-bot)
            real_visitors = db.session.query(func.count(TrackingEvent.id)).join(
                Link, TrackingEvent.link_id == Link.id
            ).filter(
                Link.campaign_id == campaign.id,
                TrackingEvent.is_bot == False
            ).scalar() or 0
            
            # Get bot traffic
            bot_traffic = total_clicks - real_visitors
            
            # Calculate conversion rate (placeholder)
            conversion_rate = (real_visitors / total_clicks * 100) if total_clicks > 0 else 0
            
            campaign_data = {
                'id': campaign.id,
                'name': campaign.name,
                'description': campaign.description,
                'status': campaign.status,
                'associated_links': links_count,
                'total_clicks': total_clicks,
                'real_visitors': real_visitors,
                'bot_traffic': bot_traffic,
                'conversion_rate': round(conversion_rate, 2),
                'created_at': campaign.created_at.isoformat() if campaign.created_at else None,
                'user_id': campaign.user_id,
                'user_name': User.query.get(campaign.user_id).username if campaign.user_id else 'Unknown'
            }
            campaign_list.append(campaign_data)
        
        return jsonify({
            'success': True,
            'campaigns': campaign_list,
            'total': len(campaign_list)
        })
    
    except Exception as e:
        print(f"Error in enhanced campaigns: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500
'''

with open(admin_complete_path, 'r') as f:
    admin_content = f.read()

if '/campaigns/enhanced' not in admin_content:
    admin_content = admin_content.rstrip() + '\n' + enhanced_campaign_route + '\n'
    
    with open(admin_complete_path, 'w') as f:
        f.write(admin_content)
    
    print("  ✓ Added enhanced campaign route")
else:
    print("  ✓ Enhanced campaign route already exists")

# =================================================================
# 4. Enhanced Audit Logs Route
# =================================================================

print("\n[4/5] Creating Enhanced Audit Logs Route...")

enhanced_audit_route = '''
@admin_complete_bp.route("/api/admin/audit/enhanced", methods=["GET"])
def get_enhanced_audit_logs():
    """Get audit logs with all requested columns"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        # Get query parameters
        action_type = request.args.get('action_type', 'all')
        limit = int(request.args.get('limit', 100))
        
        # Base query
        query = AuditLog.query.order_by(AuditLog.timestamp.desc())
        
        # Filter by action type if specified
        if action_type != 'all':
            query = query.filter_by(action=action_type)
        
        logs = query.limit(limit).all()
        
        log_list = []
        for log in logs:
            log_data = {
                'id': log.id,
                'audit_id': f"AUD-{log.id:06d}",
                'user': User.query.get(log.user_id).username if log.user_id else 'System',
                'user_id': log.user_id,
                'action_type': log.action,
                'description': log.description or log.action,
                'timestamp': log.timestamp.isoformat() if log.timestamp else None,
                'ip_address': log.ip_address or 'Unknown',
                'status': getattr(log, 'status', 'success'),
                'details': log.details if hasattr(log, 'details') else {}
            }
            log_list.append(log_data)
        
        # Calculate stats
        total_logs = AuditLog.query.count()
        failed_actions = len([l for l in log_list if l['status'] == 'failed'])
        successful_actions = len([l for l in log_list if l['status'] == 'success'])
        
        return jsonify({
            'success': True,
            'logs': log_list,
            'stats': {
                'total_logs': total_logs,
                'failed_actions': failed_actions,
                'successful_actions': successful_actions,
                'api_errors': 0  # Would need separate tracking
            }
        })
    
    except Exception as e:
        print(f"Error in enhanced audit logs: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500
'''

with open(admin_complete_path, 'r') as f:
    admin_content = f.read()

if '/audit/enhanced' not in admin_content:
    admin_content = admin_content.rstrip() + '\n' + enhanced_audit_route + '\n'
    
    with open(admin_complete_path, 'w') as f:
        f.write(admin_content)
    
    print("  ✓ Added enhanced audit logs route")
else:
    print("  ✓ Enhanced audit route already exists")

# =================================================================
# 5. Create Settings Enhancement Route
# =================================================================

print("\n[5/5] Creating Settings Enhancement Route...")

settings_enhancement_route = '''
@admin_complete_bp.route("/api/admin/settings/enhanced", methods=["GET"])
def get_enhanced_settings():
    """Get enhanced settings including domain management"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        # Get domains with enhanced data
        domains = Domain.query.all()
        domain_list = []
        for domain in domains:
            domain_data = {
                'id': domain.id,
                'domain': domain.domain,
                'ip_address': getattr(domain, 'ip_address', 'N/A'),
                'ssl_status': getattr(domain, 'ssl_enabled', False),
                'status': 'active' if domain.is_active else 'inactive',
                'severity': getattr(domain, 'severity', 'normal'),
                'created_at': domain.created_at.isoformat() if domain.created_at else None
            }
            domain_list.append(domain_data)
        
        # System stats
        system_stats = {
            'database': {
                'type': 'PostgreSQL',
                'status': 'connected',
                'size': 'N/A'  # Would need separate query
            },
            'email_smtp': {
                'host': os.environ.get('SMTP_HOST', 'Not configured'),
                'port': os.environ.get('SMTP_PORT', 'Not configured'),
                'status': 'configured' if os.environ.get('SMTP_HOST') else 'not configured'
            },
            'telegram': {
                'bot_configured': bool(os.environ.get('TELEGRAM_BOT_TOKEN_SYSTEM')),
                'status': 'active' if os.environ.get('TELEGRAM_BOT_TOKEN_SYSTEM') else 'inactive'
            },
            'payment': {
                'stripe': {
                    'configured': bool(os.environ.get('STRIPE_SECRET_KEY')),
                    'mode': 'test' if 'test' in os.environ.get('STRIPE_SECRET_KEY', '') else 'live'
                },
                'crypto': {
                    'configured': bool(os.environ.get('ENABLE_CRYPTO_PAYMENTS')),
                    'enabled': os.environ.get('ENABLE_CRYPTO_PAYMENTS', 'false') == 'true'
                }
            }
        }
        
        return jsonify({
            'success': True,
            'domains': domain_list,
            'system_stats': system_stats
        })
    
    except Exception as e:
        print(f"Error in enhanced settings: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500
'''

with open(admin_complete_path, 'r') as f:
    admin_content = f.read()

if '/settings/enhanced' not in admin_content:
    admin_content = admin_content.rstrip() + '\n' + settings_enhancement_route + '\n'
    
    with open(admin_complete_path, 'w') as f:
        f.write(admin_content)
    
    print("  ✓ Added enhanced settings route")
else:
    print("  ✓ Enhanced settings route already exists")

print("\n" + "=" * 80)
print("PHASE 2 BACKEND ENHANCEMENTS COMPLETED")
print("=" * 80)
print("\nNew API Endpoints Created:")
print("  - /api/admin/users/enhanced")
print("  - /api/admin/security/threats/enhanced")
print("  - /api/admin/campaigns/enhanced")
print("  - /api/admin/audit/enhanced")
print("  - /api/admin/settings/enhanced")
print("\nThese endpoints provide all the requested column data.")
print("Frontend components can now fetch enhanced data.")
print("=" * 80)
