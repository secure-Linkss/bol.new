"""
SQLAlchemy Model for Security Threats
"""
from datetime import datetime
from src.models.user import db

class SecurityThreat(db.Model):
    __tablename__ = 'security_threats'
    
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'))
    email = db.Column(db.String(255))
    ip_address = db.Column(db.String(45), nullable=False)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    isp = db.Column(db.String(255))
    user_agent = db.Column(db.Text)
    threat_type = db.Column(db.String(50), nullable=False)  # proxy, bot, rapid_clicks, vpn, etc.
    threat_level = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    threat_score = db.Column(db.Integer, default=0)
    flag_reason = db.Column(db.Text)
    is_blocked = db.Column(db.Boolean, default=False)
    is_whitelisted = db.Column(db.Boolean, default=False)
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    occurrence_count = db.Column(db.Integer, default=1)
    additional_data = db.Column(db.Text)
    
    # Relationships
    link = db.relationship('Link', backref='threats')
    
    def to_dict(self):
        return {
            'id': self.id,
            'link_id': self.link_id,
            'email': self.email,
            'ip_address': self.ip_address,
            'country': self.country,
            'city': self.city,
            'isp': self.isp,
            'user_agent': self.user_agent,
            'threat_type': self.threat_type,
            'threat_level': self.threat_level,
            'threat_score': self.threat_score,
            'flag_reason': self.flag_reason,
            'is_blocked': self.is_blocked,
            'is_whitelisted': self.is_whitelisted,
            'first_seen': self.first_seen.isoformat() if self.first_seen else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'occurrence_count': self.occurrence_count,
            'additional_data': self.additional_data
        }
