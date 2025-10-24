#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require'
os.environ['SECRET_KEY'] = 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE'

from flask import Flask
from src.database import db
from src.models.user import User
from src.models.link import Link
from src.models.campaign import Campaign
from src.models.tracking_event import TrackingEvent

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

db.init_app(app)

with app.app_context():
    print("="*80)
    print("🔍 QUICK DATABASE AUDIT")
    print("="*80)
    
    # Check Brain user
    brain_users = User.query.filter(
        (User.username == 'Brain') | (User.email.like('%brain%'))
    ).all()
    
    print(f"\n✅ Found {len(brain_users)} Brain user(s)")
    
    for user in brain_users:
        print(f"\n📊 User: {user.username} (ID: {user.id})")
        print(f"   Email: {user.email}")
        print(f"   Role: {user.role}")
        print(f"   Status: {user.status}")
        print(f"   Plan: {user.plan_type}")
        print(f"   Last Login: {user.last_login}")
        print(f"   Login Count: {user.login_count}")
        
        # Get links for this user
        user_links = Link.query.filter_by(user_id=user.id).all()
        print(f"\n   📎 Total Links: {len(user_links)}")
        
        # Get unique campaigns
        campaigns_from_links = db.session.query(Link.campaign_name).filter(
            Link.user_id == user.id,
            Link.campaign_name.isnot(None),
            Link.campaign_name != ''
        ).distinct().all()
        
        print(f"   📁 Unique Campaigns (from links): {len(campaigns_from_links)}")
        
        if campaigns_from_links:
            for (camp_name,) in campaigns_from_links:
                link_count = Link.query.filter_by(
                    user_id=user.id,
                    campaign_name=camp_name
                ).count()
                print(f"      • {camp_name}: {link_count} link(s)")
        
        # Check campaigns table
        campaigns_in_table = Campaign.query.filter_by(owner_id=user.id).all()
        print(f"\n   📋 Campaigns in 'campaigns' table: {len(campaigns_in_table)}")
        
        if campaigns_in_table:
            for camp in campaigns_in_table:
                print(f"      • {camp.name} (ID: {camp.id}, Status: {camp.status})")
        
        # Check tracking events
        link_ids = [link.id for link in user_links]
        if link_ids:
            total_events = TrackingEvent.query.filter(
                TrackingEvent.link_id.in_(link_ids)
            ).count()
            
            unique_ips = db.session.query(TrackingEvent.ip_address).filter(
                TrackingEvent.link_id.in_(link_ids)
            ).distinct().count()
            
            email_captures = TrackingEvent.query.filter(
                TrackingEvent.link_id.in_(link_ids),
                TrackingEvent.captured_email.isnot(None)
            ).count()
            
            print(f"\n   📈 Tracking Events:")
            print(f"      Total Events: {total_events}")
            print(f"      Unique IPs: {unique_ips}")
            print(f"      Email Captures: {email_captures}")
    
    # Overall stats
    print("\n" + "="*80)
    print("📊 OVERALL DATABASE STATISTICS")
    print("="*80)
    print(f"Total Users: {User.query.count()}")
    print(f"Total Links: {Link.query.count()}")
    print(f"Total Campaigns: {Campaign.query.count()}")
    print(f"Total Tracking Events: {TrackingEvent.query.count()}")
    
    print("\n✅ Audit complete!")
