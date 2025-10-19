"""
SQLAlchemy Model for Subscription Verifications
"""
from datetime import datetime
from src.models.user import db

class SubscriptionVerification(db.Model):
    __tablename__ = 'subscription_verifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(10), default='USD')
    tx_hash = db.Column(db.String(255))
    payment_method = db.Column(db.String(50))
    proof_url = db.Column(db.Text)
    proof_screenshot = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    rejection_reason = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='subscription_requests')
    verifier = db.relationship('User', foreign_keys=[verified_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_type': self.plan_type,
            'amount': float(self.amount) if self.amount else None,
            'currency': self.currency,
            'tx_hash': self.tx_hash,
            'payment_method': self.payment_method,
            'proof_url': self.proof_url,
            'proof_screenshot': self.proof_screenshot,
            'status': self.status,
            'requested_at': self.requested_at.isoformat() if self.requested_at else None,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'verified_by': self.verified_by,
            'rejection_reason': self.rejection_reason,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'notes': self.notes
        }
