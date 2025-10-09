from flask import Blueprint, request, jsonify, session
from src.models.link import Link
from src.models.tracking_event import TrackingEvent
from src.models.campaign import Campaign
from src.models.user import User, db
from sqlalchemy import func, desc
from functools import wraps
from datetime import datetime, timedelta
import json

analytics_bp = Blueprint("analytics", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function

@analytics_bp.route("/analytics/dashboard", methods=["GET"])
@login_required
def get_dashboard_analytics():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Authentication required"}), 401
    
    try:
        period = request.args.get("period", "7")  # Default to 7 days
        days = int(period)
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get user's links
        user_links = Link.query.filter_by(user_id=user_id).all()
        link_ids = [link.id for link in user_links]
        
        if not link_ids:
            # Return empty analytics if no links
            return jsonify({
                "analytics": {
                    "totalLinks": 0,
                    "totalClicks": 0,
                    "realVisitors": 0,
                    "capturedEmails": 0,
                    "activeLinks": 0,
                    "conversionRate": 0,
                    "avgClicksPerLink": 0
                },
                "campaigns": [],
                "countries": [],
                "emails": []
            })
        
        # Get tracking events for the period
        events = TrackingEvent.query.filter(
            TrackingEvent.link_id.in_(link_ids),
            TrackingEvent.timestamp >= start_date
        ).all()
        
        # Calculate analytics
        total_links = len(user_links)
        total_clicks = len(events)
        real_visitors = len(set(event.ip_address for event in events))
        captured_emails = len([e for e in events if e.captured_email])
        active_links = len([link for link in user_links if link.status == "active"])
        conversion_rate = (captured_emails / total_clicks * 100) if total_clicks > 0 else 0
        avg_clicks_per_link = total_clicks / total_links if total_links > 0 else 0
        
        # Get country data
        country_stats = {}
        for event in events:
            country = event.country or "Unknown"
            if country not in country_stats:
                country_stats[country] = {"clicks": 0, "emails": 0}
            country_stats[country]["clicks"] += 1
            if event.captured_email:
                country_stats[country]["emails"] += 1
        
        # Convert to list and add flags/percentages
        country_flags = {
            "United States": "🇺🇸",
            "United Kingdom": "🇬🇧", 
            "Canada": "🇨🇦",
            "Germany": "🇩🇪",
            "France": "🇫🇷",
            "Australia": "🇦🇺",
            "Unknown": "🌍"
        }
        
        countries = []
        for country, stats in country_stats.items():
            percentage = (stats["clicks"] / total_clicks * 100) if total_clicks > 0 else 0
            countries.append({
                "country": country,
                "flag": country_flags.get(country, "🌍"),
                "clicks": stats["clicks"],
                "emails": stats["emails"],
                "percentage": round(percentage, 1),
                "code": country[:2].upper()
            })
        
        countries.sort(key=lambda x: x["clicks"], reverse=True)
        
        # Get campaign data (using links as campaigns)
        campaigns = []
        for link in user_links:
            link_events = [e for e in events if e.link_id == link.id]
            link_clicks = len(link_events)
            link_emails = len([e for e in link_events if e.captured_email])
            link_visitors = len(set(e.ip_address for e in link_events))
            link_conversion = (link_emails / link_clicks * 100) if link_clicks > 0 else 0
            
            campaigns.append({
                "id": f"camp_{link.id:03d}",
                "name": link.campaign_name or f"Campaign {link.short_code}",
                "trackingId": link.short_code,
                "status": "active" if link.status == "active" else "paused",
                "clicks": link_clicks,
                "visitors": link_visitors,
                "emails": link_emails,
                "conversionRate": round(link_conversion, 1),
                "created": link.created_at.isoformat() if link.created_at else None
            })
        
        campaigns.sort(key=lambda x: x["clicks"], reverse=True)
        
        # Get recent email captures
        email_events = [e for e in events if e.captured_email]
        email_events.sort(key=lambda x: x.timestamp, reverse=True)
        
        emails = []
        for event in email_events[:20]:  # Last 20 captures
            link = next((l for l in user_links if l.id == event.link_id), None)
            emails.append({
                "email": event.captured_email,
                "campaign": link.campaign_name if link else "Unknown Campaign",
                "trackingId": link.short_code if link else "Unknown",
                "country": event.country or "Unknown",
                "captured": event.timestamp.isoformat() if event.timestamp else None
            })
        
        return jsonify({
            "analytics": {
                "totalLinks": total_links,
                "totalClicks": total_clicks,
                "realVisitors": real_visitors,
                "capturedEmails": captured_emails,
                "activeLinks": active_links,
                "conversionRate": round(conversion_rate, 1),
                "avgClicksPerLink": round(avg_clicks_per_link, 1)
            },
            "campaigns": campaigns,
            "countries": countries,
            "emails": emails
        })
        
    except Exception as e:
        print(f"Error fetching dashboard analytics: {e}")
        return jsonify({"error": str(e)}), 500

@analytics_bp.route("/analytics/realtime", methods=["GET"])
@login_required
def get_realtime_analytics():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Authentication required"}), 401
    
    try:
        # Get user's links
        user_links = Link.query.filter_by(user_id=user_id).all()
        link_ids = [link.id for link in user_links]
        
        if not link_ids:
            return jsonify({
                "clicksToday": 0,
                "visitorsOnline": 0,
                "lastActivity": None,
                "topCountryToday": None
            })
        
        # Get today's events
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_events = TrackingEvent.query.filter(
            TrackingEvent.link_id.in_(link_ids),
            TrackingEvent.timestamp >= today
        ).all()
        
        # Get last activity
        last_event = TrackingEvent.query.filter(
            TrackingEvent.link_id.in_(link_ids)
        ).order_by(desc(TrackingEvent.timestamp)).first()
        
        # Calculate realtime stats
        clicks_today = len(today_events)
        
        # Consider visitors "online" if they visited in the last 5 minutes
        five_minutes_ago = datetime.now() - timedelta(minutes=5)
        recent_events = TrackingEvent.query.filter(
            TrackingEvent.link_id.in_(link_ids),
            TrackingEvent.timestamp >= five_minutes_ago
        ).all()
        visitors_online = len(set(event.ip_address for event in recent_events))
        
        # Get top country today
        country_stats = {}
        for event in today_events:
            country = event.country or "Unknown"
            country_stats[country] = country_stats.get(country, 0) + 1
        
        top_country = max(country_stats.items(), key=lambda x: x[1])[0] if country_stats else None
        
        return jsonify({
            "clicksToday": clicks_today,
            "visitorsOnline": visitors_online,
            "lastActivity": last_event.timestamp.isoformat() if last_event and last_event.timestamp else None,
            "topCountryToday": top_country
        })
        
    except Exception as e:
        print(f"Error fetching realtime analytics: {e}")
        return jsonify({"error": str(e)}), 500

@analytics_bp.route("/analytics/performance", methods=["GET"])
@login_required
def get_performance_data():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Authentication required"}), 401
    
    try:
        period = request.args.get("period", "7")
        days = int(period)
        
        user_links = Link.query.filter_by(user_id=user_id).all()
        link_ids = [link.id for link in user_links]
        
        if not link_ids:
            return jsonify({"performanceData": []})
        
        # Generate daily performance data
        performance_data = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            day_events = TrackingEvent.query.filter(
                TrackingEvent.link_id.in_(link_ids),
                TrackingEvent.timestamp >= day_start,
                TrackingEvent.timestamp < day_end
            ).all()
            
            clicks = len(day_events)
            visitors = len(set(event.ip_address for event in day_events))
            emails = len([e for e in day_events if e.captured_email])
            
            performance_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "clicks": clicks,
                "visitors": visitors,
                "emails": emails
            })
        
        performance_data.reverse()  # Oldest first
        
        return jsonify({"performanceData": performance_data})
        
    except Exception as e:
        print(f"Error fetching performance data: {e}")
        return jsonify({"error": "Failed to fetch performance data"}), 500



@analytics_bp.route("/analytics/summary", methods=["GET"])
@login_required
def get_analytics_summary():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Authentication required"}), 401
    
    try:
        # Get user's links
        user_links = Link.query.filter_by(user_id=user_id).all()
        link_ids = [link.id for link in user_links]
        
        if not link_ids:
            return jsonify({
                "totalClicks": 0,
                "realVisitors": 0,
                "botsBlocked": 0
            })
        
        # Get tracking events
        total_clicks = TrackingEvent.query.filter(TrackingEvent.link_id.in_(link_ids)).count()
        real_visitors = TrackingEvent.query.filter(
            TrackingEvent.link_id.in_(link_ids),
            TrackingEvent.is_bot == False
        ).count()
        bots_blocked = TrackingEvent.query.filter(
            TrackingEvent.link_id.in_(link_ids),
            TrackingEvent.is_bot == True
        ).count()
        
        return jsonify({
            "totalClicks": total_clicks,
            "realVisitors": real_visitors,
            "botsBlocked": bots_blocked
        })
        
    except Exception as e:
        print(f"Error fetching analytics summary: {e}")
        return jsonify({"error": "Failed to fetch analytics"}), 500

@analytics_bp.route("/analytics/overview", methods=["GET"])
@login_required
def get_analytics_overview_comprehensive():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Authentication required"}), 401
    
    try:
        period = request.args.get("period", "7")  # Default to 7 days
        days = int(period)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        user_links = Link.query.filter_by(user_id=user_id).all()
        link_ids = [link.id for link in user_links]
        
        if not link_ids:
            return jsonify({
                "totalClicks": 0,
                "uniqueVisitors": 0,
                "conversionRate": 0,
                "bounceRate": 0,
                "capturedEmails": 0,
                "activeLinks": 0,
                "avgSessionDuration": 0,
                "topCampaigns": [],
                "devices": [],
                "countries": [],
                "performanceData": []
            })
        
        events = TrackingEvent.query.filter(
            TrackingEvent.link_id.in_(link_ids),
            TrackingEvent.timestamp >= start_date
        ).all()
        
        # --- Calculate main analytics --- 
        total_clicks = len(events)
        unique_visitors = len(set(event.ip_address for event in events if not event.is_bot))
        captured_emails = len([e for e in events if e.captured_email])
        active_links = len([link for link in user_links if link.status == "active"])
        
        conversion_rate = (captured_emails / total_clicks * 100) if total_clicks > 0 else 0
        
        # Placeholder for bounce rate and avg session duration (requires more complex logic/data)
        bounce_rate = 0 # This would require tracking page exits or time on page
        avg_session_duration = 0 # This would require session tracking

        # --- Top Campaigns --- 
        campaign_stats = {}
        for link in user_links:
            link_events = [e for e in events if e.link_id == link.id]
            link_clicks = len(link_events)
            link_emails = len([e for e in link_events if e.captured_email])
            link_conversion = (link_emails / link_clicks * 100) if link_clicks > 0 else 0
            
            campaign_stats[link.id] = {
                "name": link.campaign_name or f"Campaign {link.short_code}",
                "clicks": link_clicks,
                "conversions": link_emails,
                "rate": round(link_conversion, 1),
                "status": "active" if link.status == "active" else "paused"
            }
        
        top_campaigns = sorted(campaign_stats.values(), key=lambda x: x["clicks"], reverse=True)[:5]

        # --- Device Distribution --- 
        device_stats = {}
        for event in events:
            device_type = event.device_type or "Unknown"
            device_stats[device_type] = device_stats.get(device_type, 0) + 1
        
        devices = []
        total_device_events = sum(device_stats.values())
        device_colors = {"Desktop": "#3b82f6", "Mobile": "#10b981", "Tablet": "#f59e0b", "Unknown": "#6b7280"}
        for device_type, count in device_stats.items():
            percentage = (count / total_device_events * 100) if total_device_events > 0 else 0
            devices.append({"name": device_type, "value": count, "percentage": round(percentage, 1), "color": device_colors.get(device_type, "#6b7280")})
        devices.sort(key=lambda x: x["value"], reverse=True)

        # --- Geographic Distribution --- 
        country_stats = {}
        for event in events:
            country = event.country or "Unknown"
            country_stats[country] = country_stats.get(country, 0) + 1
        
        countries = []
        total_country_events = sum(country_stats.values())
        country_flags = {
            "United States": "🇺🇸", "United Kingdom": "🇬🇧", "Canada": "🇨🇦", "Germany": "🇩🇪",
            "France": "🇫🇷", "Australia": "🇦🇺", "India": "🇮🇳", "Brazil": "🇧🇷", "Japan": "🇯🇵",
            "China": "🇨🇳", "Russia": "🇷🇺", "Mexico": "🇲🇽", "South Africa": "🇿🇦", "Unknown": "🌍"
        }
        for country, count in country_stats.items():
            percentage = (count / total_country_events * 100) if total_country_events > 0 else 0
            countries.append({"name": country, "clicks": count, "percentage": round(percentage, 1), "flag": country_flags.get(country, "🌍")})
        countries.sort(key=lambda x: x["clicks"], reverse=True)

        # --- Performance Data (daily clicks, visitors, conversions) --- 
        performance_data = []
        for i in range(days):
            date = end_date - timedelta(days=i)
            day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            day_events = [e for e in events if day_start <= e.timestamp < day_end]
            
            clicks = len(day_events)
            visitors = len(set(e.ip_address for e in day_events if not e.is_bot))
            conversions = len([e for e in day_events if e.captured_email])
            
            performance_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "clicks": clicks,
                "visitors": visitors,
                "conversions": conversions,
                "bounceRate": 0 # Placeholder
            })
        performance_data.reverse() # Oldest first

        return jsonify({
            "totalClicks": total_clicks,
            "uniqueVisitors": unique_visitors,
            "conversionRate": round(conversion_rate, 1),
            "bounceRate": bounce_rate,
            "capturedEmails": captured_emails,
            "activeLinks": active_links,
            "avgSessionDuration": avg_session_duration,
            "topCampaigns": top_campaigns,
            "devices": devices,
            "countries": countries,
            "performanceData": performance_data
        })
        
    except Exception as e:
        print(f"Error fetching comprehensive analytics overview: {e}")
        return jsonify({"error": str(e)}), 500



@analytics_bp.route("/analytics/countries", methods=["GET"])
@login_required
def get_countries_analytics():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Authentication required"}), 401
    
    try:
        period = request.args.get("period", "7")
        days = int(period)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        user_links = Link.query.filter_by(user_id=user_id).all()
        link_ids = [link.id for link in user_links]
        
        if not link_ids:
            return jsonify([])
        
        events = TrackingEvent.query.filter(
            TrackingEvent.link_id.in_(link_ids),
            TrackingEvent.timestamp >= start_date
        ).all()
        
        country_stats = {}
        for event in events:
            country = event.country or "Unknown"
            if country not in country_stats:
                country_stats[country] = {
                    "clicks": 0,
                    "emails": 0,
                    "visitors": set()
                }
            country_stats[country]["clicks"] += 1
            if event.captured_email:
                country_stats[country]["emails"] += 1
            if event.ip_address:
                country_stats[country]["visitors"].add(event.ip_address)
        
        # Convert to list format
        countries = []
        total_clicks = sum(stats["clicks"] for stats in country_stats.values())
        
        country_flags = {
            "United States": "🇺🇸", "United Kingdom": "🇬🇧", "Canada": "🇨🇦", 
            "Germany": "🇩🇪", "France": "🇫🇷", "Australia": "🇦🇺", 
            "India": "🇮🇳", "Brazil": "🇧🇷", "Japan": "🇯🇵",
            "China": "🇨🇳", "Russia": "🇷🇺", "Mexico": "🇲🇽", 
            "South Africa": "🇿🇦", "Unknown": "🌍"
        }
        
        for country, stats in country_stats.items():
            percentage = (stats["clicks"] / total_clicks * 100) if total_clicks > 0 else 0
            countries.append({
                "name": country,
                "code": country[:2].upper() if country != "Unknown" else "XX",
                "flag": country_flags.get(country, "🌍"),
                "clicks": stats["clicks"],
                "emails": stats["emails"],
                "visitors": len(stats["visitors"]),
                "percentage": round(percentage, 1)
            })
        
        countries.sort(key=lambda x: x["clicks"], reverse=True)
        return jsonify(countries)
        
    except Exception as e:
        print(f"Error fetching countries analytics: {e}")
        return jsonify({"error": str(e)}), 500

@analytics_bp.route("/analytics/cities", methods=["GET"])
@login_required
def get_cities_analytics():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Authentication required"}), 401
    
    try:
        period = request.args.get("period", "7")
        days = int(period)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        user_links = Link.query.filter_by(user_id=user_id).all()
        link_ids = [link.id for link in user_links]
        
        if not link_ids:
            return jsonify([])
        
        events = TrackingEvent.query.filter(
            TrackingEvent.link_id.in_(link_ids),
            TrackingEvent.timestamp >= start_date
        ).all()
        
        city_stats = {}
        for event in events:
            city = event.city or "Unknown"
            country = event.country or "Unknown"
            city_key = f"{city}, {country}"
            
            if city_key not in city_stats:
                city_stats[city_key] = {
                    "clicks": 0,
                    "emails": 0,
                    "visitors": set(),
                    "city": city,
                    "country": country
                }
            city_stats[city_key]["clicks"] += 1
            if event.captured_email:
                city_stats[city_key]["emails"] += 1
            if event.ip_address:
                city_stats[city_key]["visitors"].add(event.ip_address)
        
        # Convert to list format
        cities = []
        total_clicks = sum(stats["clicks"] for stats in city_stats.values())
        
        for city_key, stats in city_stats.items():
            percentage = (stats["clicks"] / total_clicks * 100) if total_clicks > 0 else 0
            cities.append({
                "name": city_key,
                "city": stats["city"],
                "country": stats["country"],
                "clicks": stats["clicks"],
                "emails": stats["emails"],
                "visitors": len(stats["visitors"]),
                "percentage": round(percentage, 1)
            })
        
        cities.sort(key=lambda x: x["clicks"], reverse=True)
        return jsonify(cities)
        
    except Exception as e:
        print(f"Error fetching cities analytics: {e}")
        return jsonify({"error": str(e)}), 500
