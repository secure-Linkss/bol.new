from flask import Blueprint, request, redirect, jsonify, make_response, render_template_string
from src.models.link import Link
from src.models.tracking_event import TrackingEvent
from src.models.user import db
from src.models.notification import Notification
from src.utils.user_agent_parser import parse_user_agent, generate_unique_id
from src.services.antibot import antibot_service
from datetime import datetime
import requests
import json
import base64
import os

track_bp = Blueprint("track", __name__)

def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0].strip()
    elif request.headers.get("X-Real-IP"):
        return request.headers.get("X-Real-IP")
    else:
        return request.remote_addr

def get_user_agent():
    return request.headers.get("User-Agent", "")

def check_social_referrer():
    """Check if the request comes from a social media platform"""
    referrer = request.headers.get("Referer", "").lower()
    social_platforms = [
        "facebook.com", "twitter.com", "instagram.com", "linkedin.com", 
        "youtube.com", "tiktok.com", "snapchat.com", "pinterest.com",
        "reddit.com", "tumblr.com", "whatsapp.com", "telegram.org"
    ]
    
    for platform in social_platforms:
        if platform in referrer:
            return {
                "is_social": True,
                "platform": platform,
                "referrer": referrer
            }
    
    return {
        "is_social": False,
        "platform": None,
        "referrer": referrer
    }

def check_geo_targeting(link, geo_data):
    """Check if the request meets geo-targeting requirements"""
    # For now, return True (allow all). Can be enhanced later
    return {
        "allowed": True,
        "reason": "No geo restrictions"
    }

def get_geolocation(ip_address):
    """Enhanced geolocation with zip code and detailed ISP information"""
    try:
        # Using ip-api.com for comprehensive geolocation data
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,mobile,proxy,hosting,query", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "country": data.get("country", "Unknown"),
                    "country_code": data.get("countryCode", "Unknown"),
                    "region": data.get("regionName", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "zip_code": data.get("zip"),
                    "latitude": data.get("lat"),
                    "longitude": data.get("lon"),
                    "timezone": data.get("timezone", "Unknown"),
                    "isp": data.get("isp", "Unknown"),
                    "organization": data.get("org", "Unknown"),
                    "as_number": data.get("as", "Unknown"),
                    "as_name": data.get("asname", "Unknown"),
                    "is_mobile": data.get("mobile", False),
                    "is_proxy": data.get("proxy", False),
                    "is_hosting": data.get("hosting", False)
                }
    except Exception as e:
        print(f"Geolocation error: {e}")
    
    return {
        "country": "Unknown",
        "country_code": "Unknown",
        "region": "Unknown",
        "city": "Unknown",
        "zip_code": "Unknown",
        "latitude": None,
        "longitude": None,
        "timezone": "Unknown",
        "isp": "Unknown",
        "organization": "Unknown",
        "as_number": "Unknown",
        "as_name": "Unknown",
        "is_mobile": False,
        "is_proxy": False,
        "is_hosting": False
    }

def check_geo_targeting(link, geo_data):
    """Enhanced geo targeting check with allow/block logic"""
    if not link.geo_targeting_enabled:
        return {"blocked": False, "reason": None}
    
    country = geo_data.get("country", "Unknown")
    region = geo_data.get("region", "Unknown")
    city = geo_data.get("city", "Unknown")
    
    # If location is unknown, block by default
    if country == "Unknown":
        return {"blocked": True, "reason": "unknown_location"}
    
    # Parse JSON arrays
    allowed_countries = json.loads(link.allowed_countries) if link.allowed_countries else []
    blocked_countries = json.loads(link.blocked_countries) if link.blocked_countries else []
    allowed_regions = json.loads(link.allowed_regions) if link.allowed_regions else []
    blocked_regions = json.loads(link.blocked_regions) if link.blocked_regions else []
    allowed_cities = json.loads(link.allowed_cities) if link.allowed_cities else []
    blocked_cities = json.loads(link.blocked_cities) if link.blocked_cities else []
    
    if link.geo_targeting_type == "allow":
        # Allow mode: only allow specified locations
        country_allowed = not allowed_countries or country in allowed_countries
        region_allowed = not allowed_regions or region in allowed_regions
        city_allowed = not allowed_cities or city in allowed_cities
        
        if not (country_allowed and region_allowed and city_allowed):
            if not country_allowed:
                return {"blocked": True, "reason": "country_not_allowed"}
            elif not region_allowed:
                return {"blocked": True, "reason": "region_not_allowed"}
            elif not city_allowed:
                return {"blocked": True, "reason": "city_not_allowed"}
    
    else:  # block mode
        # Block mode: block specified locations
        if country in blocked_countries:
            return {"blocked": True, "reason": "country_blocked"}
        if region in blocked_regions:
            return {"blocked": True, "reason": "region_blocked"}
        if city in blocked_cities:
            return {"blocked": True, "reason": "city_blocked"}
    
    return {"blocked": False, "reason": None}

@track_bp.route("/t/<short_code>")
def track_click(short_code):
    """
    QUANTUM REDIRECT ENTRY POINT
    This replaces the basic tracking with super advanced 4-stage quantum redirect system
    """
    # Get the tracking link
    link = Link.query.filter_by(short_code=short_code).first()
    if not link:
        return "Link not found", 404
    
    # Collect client information
    ip_address = get_client_ip()
    user_agent = get_user_agent()
    timestamp = datetime.utcnow()
    referrer = request.headers.get("Referer", "")
    
    # Import quantum redirect system
    from src.services.quantum_redirect import quantum_redirect
    from src.services.live_activity_monitor import live_monitor, ActivityType
    
    # Prepare request data for antibot service
    request_data = {
        "ip_address": ip_address,
        "user_agent": user_agent,
        "headers": dict(request.headers),
        "referrer": referrer,
        "timestamp": timestamp.timestamp()
    }
    
    # Analyze request with advanced anti-bot service
    antibot_analysis = antibot_service.analyze_request(request_data)
    is_bot = antibot_analysis["is_bot"]
    bot_block_reason = antibot_analysis["blocked_reason"]
    
    # Get geolocation data
    geo_data = get_geolocation(ip_address)
    
    # Parse user agent for device and browser info
    device_info = parse_user_agent(user_agent)
    
    # Social referrer check
    social_check = check_social_referrer()
    
    # Geo targeting check
    geo_check = check_geo_targeting(link, geo_data)
    
    # Generate unique ID for this tracking event
    unique_id = request.args.get("uid") or generate_unique_id()
    
    # Determine if request should be blocked before quantum processing
    block_reason = None
    should_process = True
    
    # Apply pre-quantum blocking rules
    # Note: For now, we allow all requests unless specifically blocked
    # Social and geo checks are informational only
    if not geo_check.get("allowed", True):  # Block if geo check fails
        block_reason = geo_check.get("reason", "Geographic restriction")
        should_process = False
    elif link.bot_blocking_enabled and is_bot:
        block_reason = bot_block_reason or "bot_detected_advanced"
        should_process = False
    
    # Record initial tracking event
    try:
        event = TrackingEvent(
            event_type="click",
            link_id=link.id,
            user_id=link.user_id,
            timestamp=timestamp,
            ip_address=ip_address,
            user_agent=user_agent,
            country=geo_data["country"],
            region=geo_data["region"],
            city=geo_data["city"],
            zip_code=geo_data["zip_code"],
            latitude=geo_data["latitude"],
            longitude=geo_data["longitude"],
            timezone=geo_data["timezone"],
            isp=geo_data["isp"],
            organization=geo_data["organization"],
            as_number=geo_data["as_number"],
            device_type=device_info["device_type"],
            browser=device_info["browser"],
            browser_version=device_info["browser_version"],
            os=device_info["os"],
            os_version=device_info["os_version"],
            status="quantum_processing" if should_process else "blocked",
            blocked_reason=block_reason,
            email_opened=False,
            redirected=False,
            on_page=False,
            unique_id=unique_id,
            is_bot=is_bot,
            referrer=referrer,
            page_views=1,
            threat_score=antibot_analysis["threat_score"],
            bot_type=antibot_analysis["bot_type"],
            quantum_enabled=True,
            quantum_stage="pre_processing"
        )
        
        db.session.add(event)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        print(f"Error recording initial tracking event: {e}")
    
    # Handle pre-quantum blocking
    if not should_process:
        # Log security violation in live monitor
        live_monitor.log_activity(
            ActivityType.SECURITY_VIOLATION,
            link.user_id,
            ip_address,
            user_agent,
            {
                'violation_type': block_reason,
                'link_id': link.id,
                'short_code': short_code,
                'geo_data': geo_data,
                'device_info': device_info
            }
        )
        
        # Create a notification for the user
        try:
            notification = Notification(
                user_id=link.user_id,
                event_type="security_alert",
                message=f"Blocked a suspicious click on link '{link.title or short_code}' due to: {block_reason}",
                metadata=json.dumps({
                    'link_id': link.id,
                    'short_code': short_code,
                    'reason': block_reason,
                    'ip_address': ip_address,
                    'user_agent': user_agent
                })
            )
            db.session.add(notification)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error creating security notification: {e}")
        
        # Redirect to a safe page or show a blocked message
        return render_template_string("<h1>Request Blocked</h1><p>Your request has been identified as suspicious and was blocked for security reasons.</p>"), 403

    # If not blocked, proceed with quantum redirect
    try:
        # Pass all relevant data to the quantum redirect system
        redirect_url = quantum_redirect(
            link=link,
            request_data={
                "ip_address": ip_address,
                "user_agent": user_agent,
                "geo_data": geo_data,
                "device_info": device_info,
                "social_check": social_check,
                "unique_id": unique_id
            }
        )
        
        # Update tracking event with final status
        event.status = "redirected"
        event.redirected = True
        db.session.commit()
        
        # Log successful redirect in live monitor
        live_monitor.log_activity(
            ActivityType.LINK_CLICK,
            link.user_id,
            ip_address,
            user_agent,
            {
                'link_id': link.id,
                'short_code': short_code,
                'destination': redirect_url
            }
        )
        
        # Create notification for the user
        try:
            notification = Notification(
                user_id=link.user_id,
                event_type="link_click",
                message=f"New click on link '{link.title or short_code}' from {geo_data['city']}, {geo_data['country']}",
                metadata=json.dumps({
                    'link_id': link.id,
                    'short_code': short_code,
                    'ip_address': ip_address,
                    'geo_location': f"{geo_data['city']}, {geo_data['country']}"
                })
            )
            db.session.add(notification)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error creating link click notification: {e}")
            
        return redirect(redirect_url)

    except Exception as e:
        print(f"Quantum redirect error: {e}")
        
        # Fallback to simple redirect if quantum system fails
        return redirect(link.target_url)

@track_bp.route("/t/<short_code>/qr")
def get_qr_code(short_code):
    """Generate and return a QR code for the short link"""
    link = Link.query.filter_by(short_code=short_code).first()
    if not link:
        return "Link not found", 404

    # Construct the full short URL
    short_url = f"{request.host_url}t/{short_code}"

    # Generate QR code using an external service or a library like `qrcode`
    # For simplicity, we'll use an online QR code generator API
    qr_code_api = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={short_url}"
    
    try:
        response = requests.get(qr_code_api, timeout=10)
        if response.status_code == 200:
            # Return the QR code image
            return response.content, 200, {'Content-Type': 'image/png'}
        else:
            return "Error generating QR code", 500
    except Exception as e:
        print(f"QR code generation error: {e}")
        return "Error generating QR code", 500

@track_bp.route("/pixel/<link_id>")
def track_pixel(link_id):
    """
    1x1 transparent pixel for email open tracking.
    This is a simplified version and needs to be expanded for robustness.
    """
    # Decode the link_id from base64
    try:
        decoded_id = base64.urlsafe_b64decode(link_id.encode()).decode()
        actual_link_id, unique_id = decoded_id.split('|')
    except Exception:
        return "Invalid tracking pixel", 400

    link = Link.query.get(actual_link_id)
    if not link:
        return "Link not found", 404

    # Collect client information
    ip_address = get_client_ip()
    user_agent = get_user_agent()
    timestamp = datetime.utcnow()
    
    # Get geolocation data
    geo_data = get_geolocation(ip_address)
    
    # Parse user agent for device and browser info
    device_info = parse_user_agent(user_agent)
    
    # Record the email open event
    try:
        event = TrackingEvent(
            event_type="email_open",
            link_id=link.id,
            user_id=link.user_id,
            timestamp=timestamp,
            ip_address=ip_address,
            user_agent=user_agent,
            country=geo_data["country"],
            region=geo_data["region"],
            city=geo_data["city"],
            zip_code=geo_data["zip_code"],
            latitude=geo_data["latitude"],
            longitude=geo_data["longitude"],
            timezone=geo_data["timezone"],
            isp=geo_data["isp"],
            organization=geo_data["organization"],
            as_number=geo_data["as_number"],
            device_type=device_info["device_type"],
            browser=device_info["browser"],
            browser_version=device_info["browser_version"],
            os=device_info["os"],
            os_version=device_info["os_version"],
            status="email_opened",
            email_opened=True,
            unique_id=unique_id
        )
        db.session.add(event)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error recording email open event: {e}")

    # Return a 1x1 transparent GIF
    pixel_gif = base64.b64decode("R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==")
    response = make_response(pixel_gif)
    response.headers['Content-Type'] = 'image/gif'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@track_bp.route("/track/page-view", methods=["POST"])
def track_page_view():
    """Track page views for a given link"""
    data = request.get_json()
    short_code = data.get("short_code")
    unique_id = data.get("unique_id")

    if not short_code or not unique_id:
        return jsonify({"status": "error", "message": "Missing parameters"}), 400

    link = Link.query.filter_by(short_code=short_code).first()
    if not link:
        return jsonify({"status": "error", "message": "Link not found"}), 404

    # Find the original tracking event
    event = TrackingEvent.query.filter_by(unique_id=unique_id).first()
    if not event:
        return jsonify({"status": "error", "message": "Tracking event not found"}), 404

    # Increment page view count
    event.page_views += 1
    db.session.commit()

    return jsonify({"status": "success"}), 200

@track_bp.route("/track/on-page", methods=["POST"])
def track_on_page():
    """Track if the user is still on the page"""
    data = request.get_json()
    short_code = data.get("short_code")
    unique_id = data.get("unique_id")

    if not short_code or not unique_id:
        return jsonify({"status": "error", "message": "Missing parameters"}), 400

    link = Link.query.filter_by(short_code=short_code).first()
    if not link:
        return jsonify({"status": "error", "message": "Link not found"}), 404

    event = TrackingEvent.query.filter_by(unique_id=unique_id).first()
    if not event:
        return jsonify({"status": "error", "message": "Tracking event not found"}), 404

    event.on_page = True
    db.session.commit()

    return jsonify({"status": "success"}), 200

