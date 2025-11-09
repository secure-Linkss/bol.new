import os
import stripe
from flask import jsonify
from src.database import db
from src.models.user import User
from src.services.monitoring import log_event
from src.services.telegram import send_telegram_notification
from src.services.slack_notifier import send_slack_notification

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Updated plan configuration
PLAN_PRICES = {
    "weekly": {
        "price": 35,
        "interval": "week",
        "interval_count": 1,
        "days": 7
    },
    "biweekly": {
        "price": 68,
        "interval": "week",
        "interval_count": 2,
        "days": 14
    },
    "monthly": {
        "price": 150,
        "interval": "month",
        "interval_count": 1,
        "days": 30
    },
    "quarterly": {
        "price": 420,
        "interval": "month",
        "interval_count": 3,
        "days": 90
    }
}

def create_checkout_session(stripe_price_id, user_id, plan_type):
    """
    Creates a Stripe Checkout Session for a new subscription.
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=os.environ.get('STRIPE_SUCCESS_URL', 'http://localhost:3000/settings?payment=success'),
            cancel_url=os.environ.get('STRIPE_CANCEL_URL', 'http://localhost:3000/settings?payment=cancel'),
            client_reference_id=str(user_id),
            metadata={
                'user_id': str(user_id),
                'plan_type': plan_type
            }
        )
        return session
    except Exception as e:
        log_event(f"Stripe session creation failed: {e}", "ERROR")
        raise e

def handle_webhook_event(payload, sig_header):
    """
    Handles Stripe webhook events.
    """
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    if not webhook_secret:
        log_event("Stripe webhook secret not configured.", "ERROR")
        return {"msg": "Webhook secret not configured"}, 500

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        log_event(f"Invalid Stripe payload: {e}", "WARNING")
        return {"msg": "Invalid payload"}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        log_event(f"Invalid Stripe signature: {e}", "WARNING")
        return {"msg": "Invalid signature"}, 400

    event_type = event['type']
    data = event['data']
    obj = data['object']

    if event_type == 'checkout.session.completed':
        # Fulfilling the purchase
        client_reference_id = obj.get('client_reference_id')
        plan_type = obj.get('metadata', {}).get('plan_type')
        
        if client_reference_id and plan_type:
            user_id = int(client_reference_id)
            user = User.query.get(user_id)
            
            if user:
                # Update user's plan and subscription status
                user.plan_type = plan_type
                # Logic to calculate new expiry date based on plan.billing_period
                # For simplicity, let's assume a 30-day extension for now
                import datetime
                user.subscription_expiry = datetime.datetime.utcnow() + datetime.timedelta(days=30)
                db.session.commit()

                log_event(f"Stripe checkout completed. User {user_id} subscribed to {plan_type}.", "INFO")
                send_telegram_notification(f"SUCCESS: User {user_id} subscribed to {plan_type} via Stripe.", is_system=True)
                send_slack_notification(f"SUCCESS: User {user_id} subscribed to {plan_type} via Stripe.", is_system=True)
            else:
                log_event(f"Stripe checkout completed for unknown user ID: {user_id}", "ERROR")

    elif event_type == 'invoice.payment_succeeded':
        # Handle recurring payment success
        # You would typically update the subscription expiry here
        pass

    elif event_type == 'invoice.payment_failed':
        # Handle payment failure
        # You would typically notify the user and potentially downgrade the plan
        pass

    # Other events like customer.subscription.deleted, etc. should be handled here

    return {"msg": "Success"}, 200
