import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.database import db
from src.models.user import User
from src.models.subscription_verification import SubscriptionVerification
from src.models.subscription_verification_db import SubscriptionVerificationDB
from src.models.admin_settings import AdminSettings
from src.services.telegram import send_telegram_notification
from src.services.slack_notifier import send_slack_notification
from src.services.monitoring import log_event
from src.services.advanced_security_system import security_check
from src.services.antibot import antibot_check
from src.services.threat_intelligence import threat_intelligence_check
from src.services.campaign_intelligence import campaign_intelligence_check
from src.services.geospatial_intelligence import geospatial_intelligence_check
from src.services.link_intelligence_platform import link_intelligence_platform_check
from src.services.live_activity_monitor import live_activity_monitor_check
from src.services.quantum_redirect import quantum_redirect_check
from src.services.cdn_manager import cdn_manager_check
from src.services.image_optimizer import image_optimizer_check
from src.services.intelligent_notification_system import intelligent_notification_system_check
from src.api.stripe_payments import create_checkout_session, handle_webhook_event

payments_bp = Blueprint('payments', __name__)

# Updated Subscription Plans Configuration
PLANS = {
    "free": {
        "name": "Free",
        "price": 0,
        "billing_period": "forever",
        "features": ["Basic tracking", "Up to 10 links", "7 days data retention"],
        "limits": {"links": 10, "clicks": 1000}
    },
    "weekly": {
        "name": "Weekly",
        "price": 35,
        "billing_period": "week",
        "billing_interval": 1,
        "stripe_price_id": os.environ.get("STRIPE_WEEKLY_PRICE_ID", ""),
        "features": ["Advanced tracking", "Unlimited links", "30 days data retention", "Email support"],
        "limits": {"links": -1, "clicks": -1}
    },
    "biweekly": {
        "name": "Biweekly",
        "price": 68,
        "billing_period": "2weeks",
        "billing_interval": 2,
        "stripe_price_id": os.environ.get("STRIPE_BIWEEKLY_PRICE_ID", ""),
        "features": ["Advanced tracking", "Unlimited links", "60 days data retention", "Custom domains", "Priority email support"],
        "limits": {"links": -1, "clicks": -1}
    },
    "monthly": {
        "name": "Monthly",
        "price": 150,
        "billing_period": "month",
        "billing_interval": 1,
        "stripe_price_id": os.environ.get("STRIPE_MONTHLY_PRICE_ID", ""),
        "features": ["Everything in Biweekly", "90 days data retention", "API access", "Priority support"],
        "limits": {"links": -1, "clicks": -1}
    },
    "quarterly": {
        "name": "Quarterly",
        "price": 420,
        "billing_period": "month",
        "billing_interval": 3,
        "stripe_price_id": os.environ.get("STRIPE_QUARTERLY_PRICE_ID", ""),
        "features": ["Everything in Monthly", "White label", "Custom integrations", "Dedicated support", "180 days data retention"],
        "limits": {"links": -1, "clicks": -1}
    }
}

@payments_bp.route('/plans', methods=['GET'])
@jwt_required()
def get_plans():
    """
    Returns the list of available subscription plans.
    """
    try:
        # Filter out the stripe_price_id for security
        safe_plans = {k: {key: val for key, val in v.items() if key != 'stripe_price_id'} for k, v in PLANS.items()}
        return jsonify(safe_plans), 200
    except Exception as e:
        log_event(f"Error fetching plans: {e}", "ERROR")
        return jsonify({"msg": "An error occurred while fetching plans"}), 500

@payments_bp.route('/subscribe/stripe', methods=['POST'])
@jwt_required()
def subscribe_stripe():
    """
    Initiates a Stripe checkout session for a subscription.
    """
    data = request.get_json()
    plan_type = data.get('plan_type')
    user_id = get_jwt_identity()

    if plan_type not in PLANS or plan_type == 'free':
        return jsonify({"msg": "Invalid or free plan selected"}), 400

    plan = PLANS[plan_type]
    stripe_price_id = plan.get('stripe_price_id')

    if not stripe_price_id:
        return jsonify({"msg": f"Stripe Price ID not configured for {plan_type}"}), 500

    try:
        session = create_checkout_session(stripe_price_id, user_id, plan_type)
        return jsonify({"checkout_url": session.url}), 200
    except Exception as e:
        log_event(f"Stripe checkout error for user {user_id}: {e}", "ERROR")
        return jsonify({"msg": "Failed to create Stripe checkout session"}), 500

@payments_bp.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """
    Handles Stripe webhook events for subscription updates.
    """
    payload = request.data
    sig_header = request.headers.get('stripe-signature')

    try:
        response, status_code = handle_webhook_event(payload, sig_header)
        return jsonify(response), status_code
    except Exception as e:
        log_event(f"Stripe webhook error: {e}", "ERROR")
        return jsonify({"msg": "Webhook processing failed"}), 400

@payments_bp.route('/subscribe/crypto', methods=['POST'])
@jwt_required()
def subscribe_crypto():
    """
    Handles crypto payment initiation.
    """
    data = request.get_json()
    plan_type = data.get('plan_type')
    crypto_type = data.get('crypto_type')
    amount = data.get('amount')
    user_id = get_jwt_identity()

    if plan_type not in PLANS or plan_type == 'free':
        return jsonify({"msg": "Invalid or free plan selected"}), 400

    plan = PLANS[plan_type]
    admin_settings = AdminSettings.query.first()

    if crypto_type == 'bitcoin' and not admin_settings.crypto_bitcoin_address:
        return jsonify({"msg": "Bitcoin payment is not configured"}), 500
    if crypto_type == 'ethereum' and not admin_settings.crypto_ethereum_address:
        return jsonify({"msg": "Ethereum payment is not configured"}), 500

    try:
        # Create a verification record
        verification = SubscriptionVerification(
            user_id=user_id,
            plan_type=plan_type,
            payment_method='crypto',
            crypto_type=crypto_type,
            amount=amount,
            status='pending'
        )
        db.session.add(verification)
        db.session.commit()

        # Notify admin system
        admin_message = f"New PENDING Crypto Payment: User {user_id} for {plan_type} plan ({amount} {crypto_type}). Verification ID: {verification.id}"
        send_telegram_notification(admin_message, is_system=True)
        send_slack_notification(admin_message, is_system=True)

        return jsonify({
            "msg": "Crypto payment initiated. Please complete the transfer and upload a screenshot for verification.",
            "verification_id": verification.id,
            "address": admin_settings.crypto_bitcoin_address if crypto_type == 'bitcoin' else admin_settings.crypto_ethereum_address
        }), 200
    except Exception as e:
        log_event(f"Crypto payment initiation error for user {user_id}: {e}", "ERROR")
        return jsonify({"msg": "Failed to initiate crypto payment"}), 500

@payments_bp.route('/crypto/verify', methods=['POST'])
@jwt_required()
def verify_crypto_payment():
    """
    Allows user to upload a screenshot for crypto payment verification.
    """
    user_id = get_jwt_identity()
    verification_id = request.form.get('verification_id')
    screenshot_file = request.files.get('screenshot')

    if not verification_id or not screenshot_file:
        return jsonify({"msg": "Missing verification ID or screenshot"}), 400

    verification = SubscriptionVerification.query.filter_by(id=verification_id, user_id=user_id, status='pending').first()

    if not verification:
        return jsonify({"msg": "Invalid or already processed verification ID"}), 404

    try:
        # Simulate file upload and storage (e.g., to S3 or local storage)
        # In a real application, you would save the file and get a URL
        screenshot_url = f"/uploads/crypto_proofs/{verification_id}_{screenshot_file.filename}"
        # screenshot_file.save(os.path.join('/path/to/storage', screenshot_url))

        verification.screenshot_url = screenshot_url
        verification.status = 'awaiting_review'
        db.session.commit()

        # Notify admin system
        admin_message = f"Crypto Payment Proof Uploaded: User {user_id} for Verification ID {verification.id}. Status: AWAITING REVIEW. Screenshot: {screenshot_url}"
        send_telegram_notification(admin_message, is_system=True)
        send_slack_notification(admin_message, is_system=True)

        return jsonify({"msg": "Screenshot uploaded successfully. Your payment is now awaiting admin review."}), 200
    except Exception as e:
        log_event(f"Crypto payment verification error for user {user_id}: {e}", "ERROR")
        return jsonify({"msg": "Failed to upload screenshot"}), 500

@payments_bp.route('/admin/crypto/review', methods=['POST'])
@jwt_required()
def admin_review_crypto():
    """
    Admin endpoint to approve or reject crypto payment verification.
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role not in ['admin', 'main_admin']:
        return jsonify({"msg": "Access denied"}), 403

    data = request.get_json()
    verification_id = data.get('verification_id')
    action = data.get('action') # 'approve' or 'reject'

    verification = SubscriptionVerification.query.filter_by(id=verification_id, status='awaiting_review').first()

    if not verification:
        return jsonify({"msg": "Invalid or already reviewed verification ID"}), 404

    target_user = User.query.get(verification.user_id)

    try:
        if action == 'approve':
            # Update user's plan and expiry
            target_user.plan_type = verification.plan_type
            # Logic to calculate new expiry date based on plan.billing_period
            # For simplicity, let's assume a 30-day extension for now
            # In a real app, you'd use the plan details from PLANS
            import datetime
            target_user.subscription_expiry = datetime.datetime.utcnow() + datetime.timedelta(days=30)
            
            verification.status = 'approved'
            db.session.commit()

            # Notify user
            user_message = f"Your crypto payment for the {verification.plan_type} plan has been APPROVED. Your subscription is now active."
            send_telegram_notification(user_message, target_user.telegram_personal_chat_id)
            send_slack_notification(user_message, target_user.slack_webhook_url)
            log_event(f"Crypto payment approved for user {target_user.id} by admin {user_id}", "INFO")

            return jsonify({"msg": "Payment approved and user plan updated"}), 200

        elif action == 'reject':
            verification.status = 'rejected'
            db.session.commit()

            # Notify user
            user_message = f"Your crypto payment for the {verification.plan_type} plan has been REJECTED. Please contact support."
            send_telegram_notification(user_message, target_user.telegram_personal_chat_id)
            send_slack_notification(user_message, target_user.slack_webhook_url)
            log_event(f"Crypto payment rejected for user {target_user.id} by admin {user_id}", "WARNING")

            return jsonify({"msg": "Payment rejected"}), 200

        else:
            return jsonify({"msg": "Invalid action"}), 400

    except Exception as e:
        log_event(f"Admin review error for verification {verification_id}: {e}", "ERROR")
        return jsonify({"msg": "An error occurred during admin review"}), 500
