from .user import db
from datetime import datetime

class TrackingEvent(db.Model):
    __tablename__ = 'tracking_events'

    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey("links.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    event_type = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    country = db.Column(db.String(100))
    region = db.Column(db.String(100))
    city = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timezone = db.Column(db.String(100))
    isp = db.Column(db.String(255))
    organization = db.Column(db.String(255))
    as_number = db.Column(db.String(255))
    device_type = db.Column(db.String(50))
    browser = db.Column(db.String(100))
    browser_version = db.Column(db.String(100))
    os = db.Column(db.String(100))
    os_version = db.Column(db.String(100))
    referrer = db.Column(db.Text)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    additional_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="recorded") # e.g., recorded, blocked, quantum_processing
    blocked_reason = db.Column(db.String(255))
    email_opened = db.Column(db.Boolean, default=False)
    redirected = db.Column(db.Boolean, default=False)
    on_page = db.Column(db.Boolean, default=False)
    unique_id = db.Column(db.String(255), unique=True, nullable=True)
    is_bot = db.Column(db.Boolean, default=False)
    page_views = db.Column(db.Integer, default=0)
    threat_score = db.Column(db.Integer, default=0)
    bot_type = db.Column(db.String(100))
    quantum_enabled = db.Column(db.Boolean, default=False)
    quantum_stage = db.Column(db.String(100))

    def __init__(self, link_id, event_type, user_id=None, ip_address=None, user_agent=None, country=None, region=None, city=None, zip_code=None, latitude=None, longitude=None, timezone=None, isp=None, organization=None, as_number=None, device_type=None, browser=None, browser_version=None, os=None, os_version=None, referrer=None, email=None, password=None, additional_data=None, status="recorded", blocked_reason=None, email_opened=False, redirected=False, on_page=False, unique_id=None, is_bot=False, page_views=0, threat_score=0, bot_type=None, quantum_enabled=False, quantum_stage=None, timestamp=None):
        self.link_id = link_id
        self.event_type = event_type
        self.user_id = user_id
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.country = country
        self.region = region
        self.city = city
        self.zip_code = zip_code
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.isp = isp
        self.organization = organization
        self.as_number = as_number
        self.device_type = device_type
        self.browser = browser
        self.browser_version = browser_version
        self.os = os
        self.os_version = os_version
        self.referrer = referrer
        self.email = email
        self.password = password
        self.additional_data = additional_data
        self.status = status
        self.blocked_reason = blocked_reason
        self.email_opened = email_opened
        self.redirected = redirected
        self.on_page = on_page
        self.unique_id = unique_id
        self.is_bot = is_bot
        self.page_views = page_views
        self.threat_score = threat_score
        self.bot_type = bot_type
        self.quantum_enabled = quantum_enabled
        self.quantum_stage = quantum_stage
        self.created_at = timestamp if timestamp else datetime.utcnow()

    def __repr__(self):
        return f"<TrackingEvent {self.id} (Link: {self.link_id}, Type: {self.event_type})>"

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
