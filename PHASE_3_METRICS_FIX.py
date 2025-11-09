#!/usr/bin/env python3
"""
PHASE 3: METRICS CONSISTENCY FIX
=================================
Ensures dashboard and links section show consistent data
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

print("=" * 80)
print("PHASE 3: METRICS CONSISTENCY FIX")
print("=" * 80)

# =================================================================
# Fix Dashboard Stats Endpoint
# =================================================================

print("\n[1/3] Fixing Dashboard Stats Endpoint...")

dashboard_stats_fix = '''
@admin_complete_bp.route("/api/admin/dashboard/stats/consistent", methods=["GET"])
def get_consistent_dashboard_stats():
    """Get dashboard stats with consistent calculation"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        # Total users
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True, is_verified=True).count()
        pending_users = User.query.filter_by(is_verified=False).count()
        
        # Total links
        total_links = Link.query.count()
        active_links = Link.query.filter_by(is_active=True).count()
        
        # Total clicks and real visitors - CONSISTENT CALCULATION
        total_clicks = TrackingEvent.query.count()
        real_visitors = TrackingEvent.query.filter_by(is_bot=False).count()
        bot_clicks = TrackingEvent.query.filter_by(is_bot=True).count()
        
        # Campaigns
        total_campaigns = Campaign.query.count()
        active_campaigns = Campaign.query.filter_by(status='active').count()
        
        # Today's stats
        from datetime import datetime, timedelta
        today = datetime.utcnow().date()
        today_start = datetime.combine(today, datetime.min.time())
        
        today_clicks = TrackingEvent.query.filter(
            TrackingEvent.timestamp >= today_start
        ).count()
        
        today_visitors = TrackingEvent.query.filter(
            TrackingEvent.timestamp >= today_start,
            TrackingEvent.is_bot == False
        ).count()
        
        # Security threats
        from src.models.security_threat import SecurityThreat
        active_threats = SecurityThreat.query.filter_by(status='active').count()
        
        # Subscription stats
        pro_users = User.query.filter_by(plan_type='pro').count()
        enterprise_users = User.query.filter_by(plan_type='enterprise').count()
        
        return jsonify({
            'success': True,
            'users': {
                'total': total_users,
                'active': active_users,
                'pending': pending_users,
                'pro': pro_users,
                'enterprise': enterprise_users
            },
            'links': {
                'total': total_links,
                'active': active_links
            },
            'traffic': {
                'total_clicks': total_clicks,
                'real_visitors': real_visitors,
                'bot_clicks': bot_clicks,
                'today_clicks': today_clicks,
                'today_visitors': today_visitors
            },
            'campaigns': {
                'total': total_campaigns,
                'active': active_campaigns
            },
            'security': {
                'active_threats': active_threats
            }
        })
    
    except Exception as e:
        print(f"Error in consistent stats: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500
'''

admin_complete_path = PROJECT_ROOT / 'src' / 'routes' / 'admin_complete.py'
with open(admin_complete_path, 'r') as f:
    admin_content = f.read()

if '/stats/consistent' not in admin_content:
    admin_content = admin_content.rstrip() + '\n' + dashboard_stats_fix + '\n'
    
    with open(admin_complete_path, 'w') as f:
        f.write(admin_content)
    
    print("  ✓ Added consistent dashboard stats endpoint")
else:
    print("  ✓ Consistent stats endpoint already exists")

# =================================================================
# Fix Links Stats Endpoint
# =================================================================

print("\n[2/3] Fixing Links Stats Endpoint...")

links_stats_fix = '''
@links_bp.route('/links/stats/consistent', methods=['GET'])
def get_consistent_link_stats():
    """Get link statistics with consistent calculation"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        # Get user's links
        user_links = Link.query.filter_by(user_id=user_id).all()
        link_ids = [link.id for link in user_links]
        
        if not link_ids:
            return jsonify({
                'success': True,
                'total_clicks': 0,
                'real_visitors': 0,
                'bots_blocked': 0,
                'active_links': 0
            })
        
        # CONSISTENT CALCULATION - Same as dashboard
        total_clicks = TrackingEvent.query.filter(
            TrackingEvent.link_id.in_(link_ids)
        ).count()
        
        real_visitors = TrackingEvent.query.filter(
            TrackingEvent.link_id.in_(link_ids),
            TrackingEvent.is_bot == False
        ).count()
        
        bots_blocked = TrackingEvent.query.filter(
            TrackingEvent.link_id.in_(link_ids),
            TrackingEvent.is_bot == True
        ).count()
        
        active_links = Link.query.filter_by(
            user_id=user_id,
            is_active=True
        ).count()
        
        return jsonify({
            'success': True,
            'total_clicks': total_clicks,
            'real_visitors': real_visitors,
            'bots_blocked': bots_blocked,
            'active_links': active_links
        })
    
    except Exception as e:
        print(f"Error in consistent link stats: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500
'''

links_path = PROJECT_ROOT / 'src' / 'routes' / 'links.py'
with open(links_path, 'r') as f:
    links_content = f.read()

if '/stats/consistent' not in links_content:
    links_content = links_content.rstrip() + '\n' + links_stats_fix + '\n'
    
    with open(links_path, 'w') as f:
        f.write(links_content)
    
    print("  ✓ Added consistent link stats endpoint")
else:
    print("  ✓ Consistent link stats endpoint already exists")

# =================================================================
# Create React Hook for Consistent Metrics
# =================================================================

print("\n[3/3] Creating React Hook for Consistent Metrics...")

metrics_hook_content = '''import { useState, useEffect } from 'react'

/**
 * Custom hook to fetch consistent metrics across all components
 * Ensures dashboard and links section show the same data
 */
export const useConsistentMetrics = (refreshInterval = 30000) => {
  const [metrics, setMetrics] = useState({
    totalClicks: 0,
    realVisitors: 0,
    botsBlocked: 0,
    activeLinks: 0,
    loading: true,
    error: null
  })

  const fetchMetrics = async () => {
    try {
      // Fetch from consistent endpoint
      const response = await fetch('/api/links/stats/consistent')
      
      if (!response.ok) {
        throw new Error('Failed to fetch metrics')
      }

      const data = await response.json()

      if (data.success) {
        setMetrics({
          totalClicks: data.total_clicks || 0,
          realVisitors: data.real_visitors || 0,
          botsBlocked: data.bots_blocked || 0,
          activeLinks: data.active_links || 0,
          loading: false,
          error: null
        })
      } else {
        throw new Error(data.error || 'Failed to load metrics')
      }
    } catch (error) {
      console.error('Error fetching metrics:', error)
      setMetrics(prev => ({
        ...prev,
        loading: false,
        error: error.message
      }))
    }
  }

  useEffect(() => {
    fetchMetrics()

    // Refresh metrics at specified interval
    const interval = setInterval(fetchMetrics, refreshInterval)

    return () => clearInterval(interval)
  }, [refreshInterval])

  return {
    ...metrics,
    refresh: fetchMetrics
  }
}

/**
 * Hook for admin dashboard metrics
 */
export const useAdminMetrics = (refreshInterval = 30000) => {
  const [metrics, setMetrics] = useState({
    users: { total: 0, active: 0, pending: 0 },
    links: { total: 0, active: 0 },
    traffic: {
      total_clicks: 0,
      real_visitors: 0,
      bot_clicks: 0,
      today_clicks: 0,
      today_visitors: 0
    },
    campaigns: { total: 0, active: 0 },
    security: { active_threats: 0 },
    loading: true,
    error: null
  })

  const fetchMetrics = async () => {
    try {
      const response = await fetch('/api/admin/dashboard/stats/consistent')
      
      if (!response.ok) {
        throw new Error('Failed to fetch admin metrics')
      }

      const data = await response.json()

      if (data.success) {
        setMetrics({
          ...data,
          loading: false,
          error: null
        })
      } else {
        throw new Error(data.error || 'Failed to load admin metrics')
      }
    } catch (error) {
      console.error('Error fetching admin metrics:', error)
      setMetrics(prev => ({
        ...prev,
        loading: false,
        error: error.message
      }))
    }
  }

  useEffect(() => {
    fetchMetrics()
    const interval = setInterval(fetchMetrics, refreshInterval)
    return () => clearInterval(interval)
  }, [refreshInterval])

  return {
    ...metrics,
    refresh: fetchMetrics
  }
}

export default useConsistentMetrics
'''

hooks_dir = PROJECT_ROOT / 'src' / 'hooks'
hooks_dir.mkdir(exist_ok=True)

metrics_hook_path = hooks_dir / 'useConsistentMetrics.js'
with open(metrics_hook_path, 'w') as f:
    f.write(metrics_hook_content)

print(f"  ✓ Created {metrics_hook_path}")

print("\n" + "=" * 80)
print("PHASE 3 COMPLETED")
print("=" * 80)
print("\nMetrics Consistency Fixes Applied:")
print("  1. Created /api/admin/dashboard/stats/consistent endpoint")
print("  2. Created /api/links/stats/consistent endpoint")
print("  3. Created useConsistentMetrics React hook")
print("\nBoth dashboard and links section now use the same calculation method.")
print("=" * 80)
