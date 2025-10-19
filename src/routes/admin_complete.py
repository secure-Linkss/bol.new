"""
Complete Admin Panel Routes
All endpoints for Admin Panel functionality
"""
from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash
from functools import wraps
from src.models import db
from src.models.user import User
from src.models.campaign import Campaign
from src.models.audit_log import AuditLog
from src.models.link import Link
from src.models.support_ticket_db import SupportTicket, TicketMessage
from src.models.subscription_verification_db import SubscriptionVerification
from src.models.security_threat_db import SecurityThreat
from src.models.admin_settings import AdminSettings
from src.models.tracking_event import TrackingEvent
from datetime import datetime, timedelta
from sqlalchemy import func, desc

admin_complete_bp = Blueprint("admin_complete", __name__)

def get_current_user():
    """Get current user from token or session"""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        user = User.verify_token(token)
        if user:
            return user
    return None

def admin_required(f):
    """Decorator to require admin or main_admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        if user.role not in ["admin", "main_admin", "assistant_admin"]:
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

def log_admin_action(actor_id, action, target_id=None, target_type=None, details=None):
    """Log admin actions to audit_logs"""
    try:
        audit_log = AuditLog(
            actor_id=actor_id,
            action=action,
            target_id=target_id,
            target_type=target_type,
            details=details,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(audit_log)
        db.session.commit()
    except Exception as e:
        print(f"Error logging admin action: {e}")

# ============================================================================
# CAMPAIGN MANAGEMENT ROUTES
# ============================================================================

@admin_complete_bp.route("/api/admin/campaigns/all", methods=["GET"])
@admin_required
def get_all_campaigns(current_user):
    """Get all campaigns with owner information"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        status_filter = request.args.get('status', None)
        search = request.args.get('search', '')
        
        # Build query
        query = db.session.query(Campaign, User).join(User, Campaign.owner_id == User.id)
        
        # Apply filters
        if status_filter:
            query = query.filter(Campaign.status == status_filter)
        if search:
            query = query.filter(
                db.or_(
                    Campaign.name.ilike(f'%{search}%'),
                    User.username.ilike(f'%{search}%')
                )
            )
        
        # Paginate
        total = query.count()
        campaigns_data = query.order_by(Campaign.created_at.desc()).limit(per_page).offset((page - 1) * per_page).all()
        
        # Format response
        result = []
        for campaign, owner in campaigns_data:
            # Get campaign stats
            links_count = Link.query.filter_by(campaign_id=campaign.id).count()
            total_clicks = db.session.query(func.sum(Link.total_clicks)).filter(Link.campaign_id == campaign.id).scalar() or 0
            total_visitors = db.session.query(func.sum(Link.real_visitors)).filter(Link.campaign_id == campaign.id).scalar() or 0
            
            # Get email captures count
            captures_count = TrackingEvent.query.filter(
                TrackingEvent.link_id.in_(
                    db.session.query(Link.id).filter(Link.campaign_id == campaign.id)
                ),
                TrackingEvent.email.isnot(None)
            ).count()
            
            result.append({
                "id": campaign.id,
                "name": campaign.name,
                "description": campaign.description,
                "owner_id": owner.id,
                "owner_username": owner.username,
                "owner_email": owner.email,
                "status": campaign.status,
                "created_at": campaign.created_at.isoformat() if campaign.created_at else None,
                "updated_at": campaign.updated_at.isoformat() if campaign.updated_at else None,
                "links_count": links_count,
                "total_clicks": total_clicks,
                "total_visitors": total_visitors,
                "captures_count": captures_count,
                "conversion_rate": round((captures_count / total_clicks * 100) if total_clicks > 0 else 0, 2)
            })
        
        return jsonify({
            "campaigns": result,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        })
        
    except Exception as e:
        print(f"Error fetching campaigns: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/campaigns/<int:campaign_id>/details", methods=["GET"])
@admin_required
def get_campaign_details(current_user, campaign_id):
    """Get detailed campaign information including all links and tracking events"""
    try:
        campaign = Campaign.query.get_or_404(campaign_id)
        owner = User.query.get(campaign.owner_id)
        
        # Get all links for this campaign
        links = Link.query.filter_by(campaign_id=campaign_id).all()
        links_data = []
        
        for link in links:
            # Get tracking events for this link
            events = TrackingEvent.query.filter_by(link_id=link.id).order_by(TrackingEvent.created_at.desc()).limit(100).all()
            
            links_data.append({
                "id": link.id,
                "short_code": link.short_code,
                "target_url": link.target_url,
                "status": link.status,
                "created_at": link.created_at.isoformat() if link.created_at else None,
                "total_clicks": link.total_clicks or 0,
                "real_visitors": link.real_visitors or 0,
                "blocked_attempts": link.blocked_attempts or 0,
                "events": [{
                    "id": event.id,
                    "event_type": event.event_type,
                    "email": event.email,
                    "ip_address": event.ip_address,
                    "country": event.country,
                    "city": event.city,
                    "device_type": event.device_type,
                    "browser": event.browser,
                    "os": event.os,
                    "created_at": event.created_at.isoformat() if event.created_at else None
                } for event in events]
            })
        
        # Get all email captures for this campaign
        captures = db.session.query(TrackingEvent).filter(
            TrackingEvent.link_id.in_([l.id for l in links]),
            TrackingEvent.email.isnot(None)
        ).order_by(TrackingEvent.created_at.desc()).all()
        
        captures_data = [{
            "email": capture.email,
            "ip_address": capture.ip_address,
            "country": capture.country,
            "city": capture.city,
            "link_id": capture.link_id,
            "captured_at": capture.created_at.isoformat() if capture.created_at else None
        } for capture in captures]
        
        return jsonify({
            "campaign": {
                "id": campaign.id,
                "name": campaign.name,
                "description": campaign.description,
                "status": campaign.status,
                "created_at": campaign.created_at.isoformat() if campaign.created_at else None,
                "owner": {
                    "id": owner.id,
                    "username": owner.username,
                    "email": owner.email
                }
            },
            "links": links_data,
            "captures": captures_data
        })
        
    except Exception as e:
        print(f"Error fetching campaign details: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/campaigns/<int:campaign_id>/suspend", methods=["POST"])
@admin_required
def suspend_campaign(current_user, campaign_id):
    """Suspend or activate a campaign"""
    try:
        campaign = Campaign.query.get_or_404(campaign_id)
        
        # Toggle status
        new_status = 'suspended' if campaign.status == 'active' else 'active'
        campaign.status = new_status
        db.session.commit()
        
        log_admin_action(
            current_user.id,
            f"{'Suspended' if new_status == 'suspended' else 'Activated'} campaign {campaign.name}",
            campaign_id,
            "campaign"
        )
        
        return jsonify({
            "message": f"Campaign {new_status}",
            "campaign": {
                "id": campaign.id,
                "name": campaign.name,
                "status": campaign.status
            }
        })
        
    except Exception as e:
        print(f"Error suspending campaign: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/campaigns/<int:campaign_id>/delete", methods=["DELETE"])
@admin_required
def delete_campaign(current_user, campaign_id):
    """Delete a campaign and all associated data"""
    try:
        campaign = Campaign.query.get_or_404(campaign_id)
        campaign_name = campaign.name
        
        # Delete associated tracking events
        link_ids = [link.id for link in Link.query.filter_by(campaign_id=campaign_id).all()]
        if link_ids:
            TrackingEvent.query.filter(TrackingEvent.link_id.in_(link_ids)).delete(synchronize_session=False)
        
        # Delete associated links
        Link.query.filter_by(campaign_id=campaign_id).delete()
        
        # Delete campaign
        db.session.delete(campaign)
        db.session.commit()
        
        log_admin_action(
            current_user.id,
            f"Deleted campaign {campaign_name}",
            campaign_id,
            "campaign"
        )
        
        return jsonify({"message": "Campaign deleted successfully"})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting campaign: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/campaigns/<int:campaign_id>/transfer", methods=["POST"])
@main_admin_required
def transfer_campaign(current_user, campaign_id):
    """Transfer campaign ownership to another user"""
    try:
        data = request.get_json()
        new_owner_id = data.get('new_owner_id')
        
        if not new_owner_id:
            return jsonify({"error": "New owner ID required"}), 400
        
        campaign = Campaign.query.get_or_404(campaign_id)
        new_owner = User.query.get_or_404(new_owner_id)
        old_owner = User.query.get(campaign.owner_id)
        
        campaign.owner_id = new_owner_id
        db.session.commit()
        
        log_admin_action(
            current_user.id,
            f"Transferred campaign {campaign.name} from {old_owner.username} to {new_owner.username}",
            campaign_id,
            "campaign"
        )
        
        return jsonify({
            "message": "Campaign transferred successfully",
            "campaign": {
                "id": campaign.id,
                "name": campaign.name,
                "new_owner": new_owner.username
            }
        })
        
    except Exception as e:
        print(f"Error transferring campaign: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/campaigns/<int:campaign_id>/export", methods=["GET"])
@admin_required
def export_campaign_data(current_user, campaign_id):
    """Export campaign data as CSV"""
    try:
        campaign = Campaign.query.get_or_404(campaign_id)
        links = Link.query.filter_by(campaign_id=campaign_id).all()
        
        # Create CSV content
        csv_content = "Link ID,Short Code,Target URL,Total Clicks,Real Visitors,Blocked Attempts,Status,Created At\n"
        
        for link in links:
            csv_content += f"{link.id},{link.short_code},{link.target_url},{link.total_clicks},{link.real_visitors},{link.blocked_attempts},{link.status},{link.created_at}\n"
        
        # Add tracking events
        csv_content += "\n\nTracking Events\n"
        csv_content += "Event ID,Link ID,Event Type,Email,IP Address,Country,City,Device,Browser,OS,Created At\n"
        
        for link in links:
            events = TrackingEvent.query.filter_by(link_id=link.id).all()
            for event in events:
                csv_content += f"{event.id},{event.link_id},{event.event_type},{event.email or ''},{event.ip_address},{event.country},{event.city},{event.device_type},{event.browser},{event.os},{event.created_at}\n"
        
        response = make_response(csv_content)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=campaign_{campaign_id}_export.csv'
        
        log_admin_action(current_user.id, f"Exported campaign {campaign.name} data", campaign_id, "campaign")
        
        return response
        
    except Exception as e:
        print(f"Error exporting campaign: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================================================
# SECURITY & THREAT MONITORING ROUTES
# ============================================================================

@admin_complete_bp.route("/api/admin/security/threats", methods=["GET"])
@admin_required
def get_security_threats(current_user):
    """Get all security threats"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        threat_type = request.args.get('threat_type', None)
        threat_level = request.args.get('threat_level', None)
        
        query = SecurityThreat.query
        
        if threat_type:
            query = query.filter_by(threat_type=threat_type)
        if threat_level:
            query = query.filter_by(threat_level=threat_level)
        
        total = query.count()
        threats = query.order_by(SecurityThreat.last_seen.desc()).limit(per_page).offset((page - 1) * per_page).all()
        
        return jsonify({
            "threats": [threat.to_dict() for threat in threats],
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        })
        
    except Exception as e:
        print(f"Error fetching security threats: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/security/threats/<int:threat_id>/block", methods=["POST"])
@admin_required
def block_threat(current_user, threat_id):
    """Block a security threat"""
    try:
        threat = SecurityThreat.query.get_or_404(threat_id)
        threat.is_blocked = True
        db.session.commit()
        
        log_admin_action(current_user.id, f"Blocked threat {threat.ip_address}", threat_id, "security_threat")
        
        return jsonify({"message": "Threat blocked successfully"})
        
    except Exception as e:
        print(f"Error blocking threat: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/security/threats/<int:threat_id>/whitelist", methods=["POST"])
@admin_required
def whitelist_threat(current_user, threat_id):
    """Whitelist a security threat"""
    try:
        threat = SecurityThreat.query.get_or_404(threat_id)
        threat.is_whitelisted = True
        threat.is_blocked = False
        db.session.commit()
        
        log_admin_action(current_user.id, f"Whitelisted threat {threat.ip_address}", threat_id, "security_threat")
        
        return jsonify({"message": "Threat whitelisted successfully"})
        
    except Exception as e:
        print(f"Error whitelisting threat: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/security/summary", methods=["GET"])
@admin_required
def get_security_summary(current_user):
    """Get security summary statistics"""
    try:
        # Get threat counts by type
        threat_counts = db.session.query(
            SecurityThreat.threat_type,
            func.count(SecurityThreat.id)
        ).group_by(SecurityThreat.threat_type).all()
        
        # Get blocked IPs count
        blocked_count = SecurityThreat.query.filter_by(is_blocked=True).count()
        
        # Get threats by level
        threat_levels = db.session.query(
            SecurityThreat.threat_level,
            func.count(SecurityThreat.id)
        ).group_by(SecurityThreat.threat_level).all()
        
        # Get recent threats (last 24 hours)
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_threats = SecurityThreat.query.filter(SecurityThreat.last_seen >= yesterday).count()
        
        return jsonify({
            "threat_types": {t[0]: t[1] for t in threat_counts},
            "threat_levels": {t[0]: t[1] for t in threat_levels},
            "blocked_count": blocked_count,
            "recent_threats_24h": recent_threats,
            "total_threats": SecurityThreat.query.count()
        })
        
    except Exception as e:
        print(f"Error fetching security summary: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================================================
# SUBSCRIPTION & PAYMENT VERIFICATION ROUTES
# ============================================================================

@admin_complete_bp.route("/api/admin/subscriptions/pending", methods=["GET"])
@admin_required
def get_pending_subscriptions(current_user):
    """Get all pending subscription verifications"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        query = db.session.query(SubscriptionVerification, User).join(
            User, SubscriptionVerification.user_id == User.id
        ).filter(SubscriptionVerification.status == 'pending')
        
        total = query.count()
        verifications = query.order_by(SubscriptionVerification.requested_at.desc()).limit(per_page).offset((page - 1) * per_page).all()
        
        result = []
        for verification, user in verifications:
            result.append({
                "id": verification.id,
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "plan_type": verification.plan_type,
                "amount": float(verification.amount) if verification.amount else None,
                "currency": verification.currency,
                "tx_hash": verification.tx_hash,
                "payment_method": verification.payment_method,
                "proof_url": verification.proof_url,
                "proof_screenshot": verification.proof_screenshot,
                "requested_at": verification.requested_at.isoformat() if verification.requested_at else None,
                "notes": verification.notes
            })
        
        return jsonify({
            "verifications": result,
            "total": total,
            "page": page,
            "per_page": per_page
        })
        
    except Exception as e:
        print(f"Error fetching pending subscriptions: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/subscriptions/<int:verification_id>/approve", methods=["POST"])
@admin_required
def approve_subscription(current_user, verification_id):
    """Approve a subscription verification"""
    try:
        data = request.get_json()
        verification = SubscriptionVerification.query.get_or_404(verification_id)
        user = User.query.get(verification.user_id)
        
        # Get duration from request or use default
        duration_days = data.get('duration_days', 30)
        
        # Update verification
        verification.status = 'approved'
        verification.verified_at = datetime.utcnow()
        verification.verified_by = current_user.id
        verification.start_date = datetime.utcnow()
        verification.end_date = datetime.utcnow() + timedelta(days=duration_days)
        
        # Update user subscription
        user.plan_type = verification.plan_type
        user.subscription_start = verification.start_date
        user.subscription_end = verification.end_date
        user.subscription_expiry = verification.end_date
        user.status = 'active'
        
        db.session.commit()
        
        log_admin_action(
            current_user.id,
            f"Approved subscription for user {user.username}",
            verification_id,
            "subscription_verification"
        )
        
        return jsonify({
            "message": "Subscription approved successfully",
            "verification": verification.to_dict(),
            "user": user.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error approving subscription: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/subscriptions/<int:verification_id>/reject", methods=["POST"])
@admin_required
def reject_subscription(current_user, verification_id):
    """Reject a subscription verification"""
    try:
        data = request.get_json()
        verification = SubscriptionVerification.query.get_or_404(verification_id)
        user = User.query.get(verification.user_id)
        
        rejection_reason = data.get('reason', 'No reason provided')
        
        verification.status = 'rejected'
        verification.verified_at = datetime.utcnow()
        verification.verified_by = current_user.id
        verification.rejection_reason = rejection_reason
        
        db.session.commit()
        
        log_admin_action(
            current_user.id,
            f"Rejected subscription for user {user.username}: {rejection_reason}",
            verification_id,
            "subscription_verification"
        )
        
        return jsonify({
            "message": "Subscription rejected",
            "verification": verification.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error rejecting subscription: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/subscriptions/stats", methods=["GET"])
@admin_required
def get_subscription_stats(current_user):
    """Get subscription statistics"""
    try:
        # Count by status
        pending_count = SubscriptionVerification.query.filter_by(status='pending').count()
        approved_count = SubscriptionVerification.query.filter_by(status='approved').count()
        rejected_count = SubscriptionVerification.query.filter_by(status='rejected').count()
        
        # Count active subscriptions
        now = datetime.utcnow()
        active_subs = User.query.filter(
            User.subscription_expiry > now,
            User.status == 'active'
        ).count()
        
        # Count expired subscriptions
        expired_subs = User.query.filter(
            User.subscription_expiry <= now,
            User.subscription_expiry.isnot(None)
        ).count()
        
        # Count by plan type
        plan_counts = db.session.query(
            User.plan_type,
            func.count(User.id)
        ).group_by(User.plan_type).all()
        
        return jsonify({
            "pending_verifications": pending_count,
            "approved_verifications": approved_count,
            "rejected_verifications": rejected_count,
            "active_subscriptions": active_subs,
            "expired_subscriptions": expired_subs,
            "plan_distribution": {p[0]: p[1] for p in plan_counts}
        })
        
    except Exception as e:
        print(f"Error fetching subscription stats: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================================================
# SUPPORT & TICKETING ROUTES
# ============================================================================

@admin_complete_bp.route("/api/admin/tickets", methods=["GET"])
@admin_required
def get_all_tickets(current_user):
    """Get all support tickets"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        status_filter = request.args.get('status', None)
        priority_filter = request.args.get('priority', None)
        
        query = db.session.query(SupportTicket, User).join(
            User, SupportTicket.user_id == User.id
        )
        
        if status_filter:
            query = query.filter(SupportTicket.status == status_filter)
        if priority_filter:
            query = query.filter(SupportTicket.priority == priority_filter)
        
        total = query.count()
        tickets_data = query.order_by(SupportTicket.created_at.desc()).limit(per_page).offset((page - 1) * per_page).all()
        
        result = []
        for ticket, user in tickets_data:
            result.append({
                "id": ticket.id,
                "ticket_ref": ticket.ticket_ref,
                "subject": ticket.subject,
                "message": ticket.message,
                "status": ticket.status,
                "priority": ticket.priority,
                "category": ticket.category,
                "user_id": user.id,
                "username": user.username,
                "user_email": user.email,
                "created_at": ticket.created_at.isoformat() if ticket.created_at else None,
                "updated_at": ticket.updated_at.isoformat() if ticket.updated_at else None,
                "resolved_at": ticket.resolved_at.isoformat() if ticket.resolved_at else None
            })
        
        return jsonify({
            "tickets": result,
            "total": total,
            "page": page,
            "per_page": per_page
        })
        
    except Exception as e:
        print(f"Error fetching tickets: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/tickets/<int:ticket_id>", methods=["GET"])
@admin_required
def get_ticket_details(current_user, ticket_id):
    """Get detailed ticket information with all messages"""
    try:
        ticket = SupportTicket.query.get_or_404(ticket_id)
        user = User.query.get(ticket.user_id)
        
        # Get ticket messages
        messages = TicketMessage.query.filter_by(ticket_id=ticket_id).order_by(TicketMessage.created_at.asc()).all()
        
        messages_data = []
        for msg in messages:
            msg_user = User.query.get(msg.user_id)
            messages_data.append({
                "id": msg.id,
                "message": msg.message,
                "is_admin": msg.is_admin,
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
                "username": msg_user.username if msg_user else "Unknown"
            })
        
        return jsonify({
            "ticket": ticket.to_dict(),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            },
            "messages": messages_data
        })
        
    except Exception as e:
        print(f"Error fetching ticket details: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/tickets/<int:ticket_id>/reply", methods=["POST"])
@admin_required
def reply_to_ticket(current_user, ticket_id):
    """Reply to a support ticket"""
    try:
        data = request.get_json()
        message_text = data.get('message')
        
        if not message_text:
            return jsonify({"error": "Message is required"}), 400
        
        ticket = SupportTicket.query.get_or_404(ticket_id)
        
        # Create message
        message = TicketMessage(
            ticket_id=ticket_id,
            user_id=current_user.id,
            message=message_text,
            is_admin=True
        )
        
        # Update ticket status
        if ticket.status == 'pending':
            ticket.status = 'in_progress'
        ticket.updated_at = datetime.utcnow()
        
        db.session.add(message)
        db.session.commit()
        
        log_admin_action(
            current_user.id,
            f"Replied to ticket {ticket.ticket_ref}",
            ticket_id,
            "support_ticket"
        )
        
        return jsonify({
            "message": "Reply sent successfully",
            "ticket": ticket.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error replying to ticket: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/tickets/<int:ticket_id>/status", methods=["PATCH"])
@admin_required
def update_ticket_status(current_user, ticket_id):
    """Update ticket status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['pending', 'in_progress', 'resolved', 'closed']:
            return jsonify({"error": "Invalid status"}), 400
        
        ticket = SupportTicket.query.get_or_404(ticket_id)
        old_status = ticket.status
        ticket.status = new_status
        ticket.updated_at = datetime.utcnow()
        
        if new_status == 'resolved' or new_status == 'closed':
            ticket.resolved_at = datetime.utcnow()
            ticket.resolved_by = current_user.id
        
        db.session.commit()
        
        log_admin_action(
            current_user.id,
            f"Changed ticket {ticket.ticket_ref} status from {old_status} to {new_status}",
            ticket_id,
            "support_ticket"
        )
        
        return jsonify({
            "message": "Ticket status updated",
            "ticket": ticket.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating ticket status: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/tickets/<int:ticket_id>/priority", methods=["PATCH"])
@admin_required
def update_ticket_priority(current_user, ticket_id):
    """Update ticket priority"""
    try:
        data = request.get_json()
        new_priority = data.get('priority')
        
        if new_priority not in ['low', 'normal', 'high', 'critical']:
            return jsonify({"error": "Invalid priority"}), 400
        
        ticket = SupportTicket.query.get_or_404(ticket_id)
        ticket.priority = new_priority
        ticket.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        log_admin_action(
            current_user.id,
            f"Changed ticket {ticket.ticket_ref} priority to {new_priority}",
            ticket_id,
            "support_ticket"
        )
        
        return jsonify({
            "message": "Ticket priority updated",
            "ticket": ticket.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating ticket priority: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/tickets/stats", methods=["GET"])
@admin_required
def get_ticket_stats(current_user):
    """Get ticket statistics"""
    try:
        # Count by status
        status_counts = db.session.query(
            SupportTicket.status,
            func.count(SupportTicket.id)
        ).group_by(SupportTicket.status).all()
        
        # Count by priority
        priority_counts = db.session.query(
            SupportTicket.priority,
            func.count(SupportTicket.id)
        ).group_by(SupportTicket.priority).all()
        
        # Recent tickets (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_count = SupportTicket.query.filter(SupportTicket.created_at >= week_ago).count()
        
        return jsonify({
            "status_counts": {s[0]: s[1] for s in status_counts},
            "priority_counts": {p[0]: p[1] for p in priority_counts},
            "recent_tickets_7d": recent_count,
            "total_tickets": SupportTicket.query.count()
        })
        
    except Exception as e:
        print(f"Error fetching ticket stats: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================================================
# ADMIN SETTINGS ROUTES
# ============================================================================

@admin_complete_bp.route("/api/admin/settings", methods=["GET"])
@admin_required
def get_admin_settings(current_user):
    """Get all admin settings"""
    try:
        settings = AdminSettings.query.all()
        
        result = {}
        for setting in settings:
            result[setting.setting_key] = {
                "value": setting.setting_value,
                "type": setting.setting_type,
                "description": setting.description,
                "is_public": setting.is_public
            }
        
        return jsonify({"settings": result})
        
    except Exception as e:
        print(f"Error fetching admin settings: {e}")
        return jsonify({"error": str(e)}), 500

@admin_complete_bp.route("/api/admin/settings/<setting_key>", methods=["PATCH"])
@main_admin_required
def update_admin_setting(current_user, setting_key):
    """Update an admin setting (Main Admin only)"""
    try:
        data = request.get_json()
        new_value = data.get('value')
        
        setting = AdminSettings.query.filter_by(setting_key=setting_key).first()
        
        if not setting:
            return jsonify({"error": "Setting not found"}), 404
        
        old_value = setting.setting_value
        setting.setting_value = new_value
        setting.updated_at = datetime.utcnow()
        setting.updated_by = current_user.id
        
        db.session.commit()
        
        log_admin_action(
            current_user.id,
            f"Updated setting {setting_key} from '{old_value}' to '{new_value}'",
            setting.id,
            "admin_setting"
        )
        
        return jsonify({
            "message": "Setting updated successfully",
            "setting": {
                "key": setting.setting_key,
                "value": setting.setting_value
            }
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating setting: {e}")
        return jsonify({"error": str(e)}), 500
