#!/usr/bin/env python3
"""
Comprehensive Database Initialization
Ensures all tables and relationships exist in production
"""

import os
import sys
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db, User
from src.models.link import Link
from src.models.campaign import Campaign
from src.models.tracking_event import TrackingEvent
from src.models.audit_log import AuditLog
from src.models.security import SecuritySettings, BlockedIP, BlockedCountry
from src.models.support_ticket import SupportTicket
from src.models.subscription_verification import SubscriptionVerification
from src.models.notification import Notification
from src.models.domain import Domain
from src.models.security_threat import SecurityThreat

def init_database():
    """Initialize all database tables"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("ERROR: DATABASE_URL not set in environment")
        sys.exit(1)
    
    print(f"Connecting to database...")
    engine = create_engine(database_url)
    
    # Create all tables
    print("Creating all tables...")
    from api.index import app
    with app.app_context():
        db.create_all()
    
    print("✓ Database initialization complete")
    
    # Verify tables
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"
Tables created: {len(tables)}")
    for table in sorted(tables):
        print(f"  - {table}")
    
    # Create default admin if not exists
    print("
Checking default admin...")
    with app.app_context():
        if not User.query.filter_by(username="Brain").first():
            admin = User(
                username="Brain",
                email="admin@brainlinktracker.com",
                role="main_admin",
                status="active",
                is_active=True,
                is_verified=True
            )
            admin.set_password("Mayflower1!!")
            db.session.add(admin)
            db.session.commit()
            print("✓ Created default admin: Brain")
        else:
            print("✓ Default admin already exists")

if __name__ == '__main__':
    init_database()
