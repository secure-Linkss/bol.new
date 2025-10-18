# Brain Link Tracker - API Documentation

## Overview

The Brain Link Tracker API provides comprehensive access to quantum-level security, AI-powered analytics, and advanced intelligence features. All endpoints are secured with JWT authentication and feature real-time processing capabilities.

## Base URL

```
Production: https://your-domain.vercel.app
Development: http://localhost:5000
```

## Authentication

All API endpoints require JWT authentication unless otherwise specified.

```bash
# Login to get JWT token
curl -X POST /api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Use token in subsequent requests
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" /api/endpoint
```

## Quantum Redirect System

### Genesis Link (Stage 1)
```http
GET /q/<short_code>
```

**Description**: Initiates quantum redirect with cryptographic token generation

**Response**: 302 Redirect to validation hub with JWT token

**Security Features**:
- User fingerprinting (50+ data points)
- IP address validation
- User-Agent verification
- Behavioral analysis initiation

### Validation Hub (Stage 2)
```http
GET /validate?token=<jwt_token>
```

**Description**: Cryptographic verification and threat analysis

**Parameters**:
- `token` (required): JWT token from genesis link

**Security Checks**:
- Token signature verification
- IP address consistency
- User-Agent consistency
- Replay attack prevention
- Threat scoring (0-100)

### Routing Gateway (Stage 3)
```http
GET /route?token=<jwt_token>
```

**Description**: Final parameter injection and security validation

**Response**: 302 Redirect to final destination with tracking parameters

### Quantum Metrics
```http
GET /api/quantum/metrics
```

**Description**: Comprehensive quantum system performance metrics

**Response**:
```json
{
  "quantum_metrics": {
    "total_redirects": 1250,
    "successful_redirects": 1187,
    "blocked_attempts": 63,
    "success_rate_percentage": 94.96,
    "block_rate_percentage": 5.04,
    "average_processing_time": 847.3,
    "security_violations": {
      "ip_mismatch": 12,
      "ua_mismatch": 8,
      "expired_token": 15,
      "invalid_signature": 18,
      "replay_attack": 7,
      "invalid_audience": 3
    },
    "security_effectiveness": 95.2,
    "system_health": "excellent"
  },
  "database_metrics": {
    "total_quantum_events": 1250,
    "successful_quantum_events": 1187,
    "security_violations": 63,
    "success_rate": 94.96
  },
  "system_status": {
    "operational": true,
    "performance": "excellent",
    "average_processing_time": "847.30ms",
    "security_level": "quantum"
  }
}
```

### Security Dashboard
```http
GET /api/quantum/security-dashboard
```

**Description**: Real-time security analytics and threat intelligence

**Response**:
```json
{
  "threat_analysis": {
    "active_threats": 3,
    "blocked_ips": 45,
    "suspicious_patterns": 12,
    "security_score": 94.7
  },
  "behavioral_analytics": {
    "bot_detection_rate": 99.2,
    "human_verification_rate": 98.8,
    "anomaly_detection": "active"
  }
}
```

## Advanced Analytics

### Overview Analytics
```http
GET /api/analytics/overview
```

**Description**: Comprehensive analytics dashboard with AI-powered insights

**Response**:
```json
{
  "overview": {
    "total_clicks": 15420,
    "unique_visitors": 8734,
    "emails_captured": 2156,
    "conversion_rate": 24.7,
    "bounce_rate": 18.3,
    "avg_session_duration": 342.8
  },
  "performance": [
    {
      "date": "2025-10-09",
      "clicks": 1250,
      "conversions": 308,
      "bounce_rate": 15.2
    }
  ],
  "devices": {
    "desktop": {"count": 8945, "percentage": 58.0},
    "mobile": {"count": 5234, "percentage": 34.0},
    "tablet": {"count": 1241, "percentage": 8.0}
  },
  "top_countries": [
    {"country": "United States", "clicks": 4567, "percentage": 29.6},
    {"country": "United Kingdom", "clicks": 2134, "percentage": 13.8}
  ]
}
```

### Geographic Intelligence
```http
GET /api/analytics/countries
```

**Description**: Advanced geospatial analytics with market intelligence

**Response**:
```json
{
  "countries": [
    {
      "country": "United States",
      "clicks": 4567,
      "percentage": 29.6,
      "conversion_rate": 28.4,
      "market_potential": "high",
      "economic_indicator": "strong",
      "engagement_score": 87.3
    }
  ],
  "market_analysis": {
    "expansion_opportunities": [
      {
        "country": "Germany",
        "potential_score": 92.1,
        "reasons": ["High engagement", "Strong economy", "Low competition"]
      }
    ],
    "performance_heatmap": {
      "high_intensity": ["US", "UK", "CA"],
      "medium_intensity": ["DE", "FR", "AU"],
      "low_intensity": ["BR", "IN", "MX"]
    }
  }
}
```

### Cities Analytics
```http
GET /api/analytics/cities
```

**Description**: City-level analytics with demographic insights

**Response**:
```json
{
  "cities": [
    {
      "city": "New York",
      "country": "United States",
      "clicks": 1234,
      "conversion_rate": 31.2,
      "demographic_score": 89.4,
      "timezone_optimization": "UTC-5"
    }
  ],
  "timezone_analysis": {
    "peak_hours": [7, 12, 15, 19],
    "optimal_posting_times": ["07:00", "15:00"],
    "engagement_patterns": {
      "morning": 78.3,
      "afternoon": 92.1,
      "evening": 85.7,
      "night": 34.2
    }
  }
}
```

## Campaign Intelligence

### Campaign Analytics
```http
GET /api/campaigns/intelligence
```

**Description**: AI-powered campaign optimization and performance analysis

**Response**:
```json
{
  "campaigns": [
    {
      "id": 1,
      "name": "Q4 Marketing Push",
      "performance_score": 87.3,
      "optimization_suggestions": [
        "Increase mobile targeting by 15%",
        "Focus on evening hours (7-9 PM)",
        "Test shorter subject lines"
      ],
      "predictive_metrics": {
        "forecasted_ctr": 3.2,
        "confidence_interval": "2.8-3.6",
        "optimal_budget_allocation": "$2,500"
      }
    }
  ],
  "ab_testing": {
    "active_tests": 3,
    "completed_tests": 12,
    "statistical_significance": 95.7,
    "winning_variants": [
      {
        "test_id": "test_001",
        "winner": "Variant B",
        "improvement": "23.4% higher CTR"
      }
    ]
  }
}
```

### Campaign Optimization
```http
POST /api/campaigns/optimize
```

**Description**: AI-powered campaign optimization recommendations

**Request Body**:
```json
{
  "campaign_id": 1,
  "optimization_goals": ["conversion_rate", "cost_efficiency"],
  "constraints": {
    "max_budget": 5000,
    "target_audience": "18-35"
  }
}
```

**Response**:
```json
{
  "optimization_plan": {
    "recommended_changes": [
      {
        "parameter": "target_age",
        "current_value": "18-65",
        "recommended_value": "25-40",
        "expected_improvement": "18% higher conversion rate"
      }
    ],
    "budget_reallocation": {
      "mobile": "60%",
      "desktop": "40%"
    },
    "timing_optimization": {
      "peak_hours": [15, 19, 21],
      "budget_distribution": "40% evening, 35% afternoon, 25% morning"
    }
  }
}
```

## Link Intelligence Platform

### Link Analysis
```http
GET /api/links/intelligence/<link_id>
```

**Description**: Comprehensive link intelligence and optimization analysis

**Response**:
```json
{
  "link_metrics": {
    "link_id": "123",
    "short_code": "abc123",
    "target_url": "https://example.com",
    "total_clicks": 1250,
    "unique_clicks": 987,
    "conversion_rate": 24.7,
    "bounce_rate": 18.3,
    "avg_session_duration": 342.8,
    "quality_scores": {
      "readability_score": 87.3,
      "seo_score": 92.1,
      "security_score": 95.8,
      "brand_consistency_score": 89.4,
      "conversion_potential_score": 91.2
    },
    "predictive_analytics": {
      "predicted_ctr": 3.2,
      "predicted_conversions": 156,
      "decay_prediction": 45.7,
      "optimal_refresh_date": "2025-11-23T10:00:00Z"
    },
    "performance_category": "excellent"
  },
  "optimization_recommendations": [
    "Improve short code readability by 12%",
    "Consider A/B testing alternative target pages",
    "Optimize for mobile conversion rate"
  ]
}
```

### Link Optimization
```http
POST /api/links/optimize
```

**Description**: Generate AI-powered link optimization suggestions

**Request Body**:
```json
{
  "link_id": "123",
  "optimization_strategy": "conversion_optimized",
  "target_metrics": ["ctr", "conversion_rate"]
}
```

**Response**:
```json
{
  "optimization_suggestions": {
    "short_codes": [
      "conv123",
      "click456",
      "best789"
    ],
    "url_optimizations": [
      "Add UTM parameters for better tracking",
      "Implement HTTPS for security boost",
      "Optimize landing page load speed"
    ],
    "ab_test_suggestions": {
      "should_test": true,
      "test_variants": [
        {
          "short_code": "test-a",
          "traffic_allocation": 0.5,
          "optimization_focus": "readability"
        },
        {
          "short_code": "test-b",
          "traffic_allocation": 0.5,
          "optimization_focus": "conversion"
        }
      ]
    }
  }
}
```

## Intelligent Notifications

### Smart Notifications
```http
GET /api/notifications/intelligent
```

**Description**: ML-powered notification feed with smart prioritization

**Parameters**:
- `limit` (optional): Number of notifications (default: 50)
- `category` (optional): Filter by category
- `priority` (optional): Filter by priority
- `unread_only` (optional): Show only unread notifications

**Response**:
```json
{
  "notifications": [
    {
      "id": "notif_001",
      "timestamp": "2025-10-09T15:30:00Z",
      "title": "High Traffic Alert",
      "message": "Campaign 'Q4 Push' receiving 300% above normal traffic",
      "category": "business",
      "priority": "high",
      "urgency_score": 87.3,
      "relevance_score": 92.1,
      "suggested_actions": [
        "Review campaign performance",
        "Check server capacity",
        "Analyze traffic sources"
      ],
      "delivered": true,
      "acknowledged": false
    }
  ],
  "intelligence_summary": {
    "total_notifications": 45,
    "noise_filtered": 12,
    "priority_breakdown": {
      "critical": 2,
      "high": 8,
      "medium": 15,
      "low": 20
    }
  }
}
```

### Notification Analytics
```http
GET /api/notifications/analytics
```

**Description**: Comprehensive notification intelligence and performance metrics

**Response**:
```json
{
  "analytics": {
    "total_notifications": 1250,
    "acknowledged_rate": 87.3,
    "resolution_rate": 92.1,
    "escalation_rate": 3.2,
    "average_response_time_seconds": 145,
    "intelligence_metrics": {
      "avg_urgency_score": 67.8,
      "avg_relevance_score": 78.4,
      "avg_noise_probability": 0.23
    },
    "category_breakdown": {
      "security": 234,
      "performance": 187,
      "business": 456,
      "system": 123,
      "campaign": 250
    }
  }
}
```

## Security & Threat Intelligence

### Threat Analysis
```http
POST /api/security/threat-analysis
```

**Description**: Real-time threat analysis with behavioral scoring

**Request Body**:
```json
{
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "fingerprint_data": {
    "canvas": "abc123...",
    "webgl": "def456...",
    "audio": "ghi789..."
  }
}
```

**Response**:
```json
{
  "threat_analysis": {
    "threat_score": 23.7,
    "risk_level": "low",
    "behavioral_score": 87.3,
    "fingerprint_uniqueness": 94.2,
    "geolocation_risk": 12.1,
    "proxy_detection": {
      "is_proxy": false,
      "proxy_type": null,
      "confidence": 98.7
    },
    "bot_detection": {
      "is_bot": false,
      "bot_type": null,
      "confidence": 99.2
    },
    "recommendations": [
      "Allow with standard monitoring",
      "No additional security measures needed"
    ]
  }
}
```

### Security Dashboard
```http
GET /api/security/dashboard
```

**Description**: Comprehensive security analytics and threat landscape

**Response**:
```json
{
  "security_overview": {
    "total_threats_detected": 156,
    "threats_blocked": 143,
    "success_rate": 91.7,
    "average_threat_score": 34.2
  },
  "threat_categories": {
    "bots": 89,
    "proxies": 34,
    "suspicious_behavior": 23,
    "geographic_anomalies": 10
  },
  "real_time_metrics": {
    "active_sessions": 234,
    "blocked_attempts_last_hour": 12,
    "security_alerts": 3
  }
}
```

## Live Activity Monitoring

### Activity Stream
```http
GET /api/activity/stream
```

**Description**: Real-time activity feed with behavioral analysis

**Parameters**:
- `limit` (optional): Number of events (default: 100)
- `real_time` (optional): Enable real-time updates

**Response**:
```json
{
  "activities": [
    {
      "id": "activity_001",
      "timestamp": "2025-10-09T15:30:00Z",
      "event_type": "link_click",
      "user_info": {
        "ip_address": "192.168.1.1",
        "country": "United States",
        "device_type": "desktop",
        "browser": "Chrome"
      },
      "link_info": {
        "short_code": "abc123",
        "campaign": "Q4 Marketing"
      },
      "behavioral_analysis": {
        "suspicion_score": 12.3,
        "engagement_score": 87.6,
        "session_quality": "high"
      },
      "quantum_metrics": {
        "processing_time": 234,
        "security_score": 94.7,
        "verification_status": "verified"
      }
    }
  ],
  "stream_metrics": {
    "events_per_second": 15.7,
    "unique_visitors": 234,
    "geographic_spread": 45,
    "device_distribution": {
      "desktop": 58.3,
      "mobile": 34.2,
      "tablet": 7.5
    }
  }
}
```

## Error Handling

All API endpoints return standardized error responses:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_TOKEN",
    "message": "JWT token is invalid or expired",
    "details": "Token signature verification failed"
  },
  "timestamp": "2025-10-09T15:30:00Z"
}
```

### Common Error Codes

- `INVALID_TOKEN` - JWT token is invalid or expired
- `INSUFFICIENT_PERMISSIONS` - User lacks required permissions
- `RATE_LIMIT_EXCEEDED` - API rate limit exceeded
- `RESOURCE_NOT_FOUND` - Requested resource doesn't exist
- `VALIDATION_ERROR` - Request data validation failed
- `SECURITY_VIOLATION` - Security policy violation detected

## Rate Limiting

API endpoints are rate-limited based on user tier:

- **Free Tier**: 1,000 requests/hour
- **Pro Tier**: 10,000 requests/hour
- **Enterprise Tier**: Unlimited

Rate limit headers are included in all responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1696867200
```

## Webhooks

Configure webhooks to receive real-time notifications:

```http
POST /api/webhooks/configure
```

**Request Body**:
```json
{
  "url": "https://your-domain.com/webhook",
  "events": ["link_click", "security_alert", "campaign_milestone"],
  "secret": "your_webhook_secret"
}
```

### Webhook Events

- `link_click` - New link click detected
- `security_alert` - Security threat detected
- `campaign_milestone` - Campaign reaches milestone
- `performance_alert` - Performance threshold exceeded
- `quantum_violation` - Quantum security violation

## SDK and Libraries

### JavaScript SDK
```javascript
import BrainLinkTracker from 'brain-link-tracker-sdk';

const tracker = new BrainLinkTracker({
  apiKey: 'your_api_key',
  baseUrl: 'https://your-domain.vercel.app'
});

// Get analytics
const analytics = await tracker.analytics.getOverview();

// Create link
const link = await tracker.links.create({
  target_url: 'https://example.com',
  campaign_id: 1
});
```

### Python SDK
```python
from brain_link_tracker import BrainLinkTracker

tracker = BrainLinkTracker(
    api_key='your_api_key',
    base_url='https://your-domain.vercel.app'
)

# Get analytics
analytics = tracker.analytics.get_overview()

# Create link
link = tracker.links.create(
    target_url='https://example.com',
    campaign_id=1
)
```

## Support

For API support and questions:
- **Documentation**: [API Docs](https://your-domain.vercel.app/docs)
- **Support Email**: api-support@brainlinktracker.com
- **GitHub Issues**: [Report API Issues](https://github.com/secure-Linkss/bol.new/issues)

---

**Last Updated**: October 2025 - Quantum Intelligence API v2.0
