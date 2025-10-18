from .user import db
from datetime import datetime

class TrackingEvent(db.Model):
    __tablename__ = 'tracking_events'

    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey("links.id"), nullable=False)  # Fixed: links instead of link
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    event_type = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    country = db.Column(db.String(100))
    region = db.Column(db.String(100))
    city = db.Column(db.String(100))
    device_type = db.Column(db.String(50))
    browser = db.Column(db.String(100))
    os = db.Column(db.String(100))
    referrer = db.Column(db.Text)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    additional_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TrackingEvent {self.id} for link {self.link_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "link_id": self.link_id,
            "user_id": self.user_id,
            "event_type": self.event_type,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "country": self.country,
            "region": self.region,
            "city": self.city,
            "device_type": self.device_type,
            "browser": self.browser,
            "os": self.os,
            "referrer": self.referrer,
            "email": self.email,
            "password": self.password,
            "additional_data": self.additional_data,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }