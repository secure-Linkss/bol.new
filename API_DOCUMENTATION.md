# Brain Link Tracker - API Documentation

## Enhanced Admin Endpoints

### User Management

#### GET /api/admin/users/enhanced
Get enhanced user list with all details.

**Response:**
```json
{
  "success": true,
  "users": [
    {
      "id": 1,
      "username": "user123",
      "email": "user@example.com",
      "role": "user",
      "status": "active",
      "account_type": "user",
      "subscription_plan": "pro",
      "subscription_status": "active",
      "payment_status": "paid",
      "date_joined": "2025-01-15T10:30:00Z",
      "last_login": "2025-10-24T08:15:00Z",
      "login_method": "email",
      "is_verified": true,
      "verification_status": "verified",
      "is_active": true,
      "total_links": 15,
      "total_clicks": 1250
    }
  ],
  "active_users": [...],
  "pending_users": [...],
  "suspended_users": [...],
  "stats": {
    "total": 100,
    "active": 85,
    "pending": 10,
    "suspended": 5,
    "admins": 3
  }
}
```

### Security Management

#### GET /api/admin/security/threats/enhanced
Get enhanced security threats with detailed information.

**Response:**
```json
{
  "success": true,
  "threats": [
    {
      "id": 1,
      "ip_address": "192.168.1.1",
      "country": "United States",
      "city": "New York",
      "threat_type": "bot",
      "severity": "high",
      "status": "active",
      "description": "Suspicious bot activity detected",
      "user_agent": "Mozilla/5.0...",
      "device": "Desktop",
      "browser": "Chrome",
      "action_taken": "blocked",
      "detected_at": "2025-10-24T10:00:00Z",
      "resolved_at": null
    }
  ],
  "bot_activity": [...],
  "stats": {
    "total_threats": 50,
    "active_threats": 10,
    "resolved_threats": 40,
    "bots_blocked": 500,
    "high_severity": 5
  }
}
```

### Campaign Management

#### GET /api/admin/campaigns/enhanced
Get enhanced campaign details.

**Response:**
```json
{
  "success": true,
  "campaigns": [
    {
      "id": 1,
      "name": "Summer Campaign",
      "description": "Summer promotion 2025",
      "status": "active",
      "associated_links": 10,
      "total_clicks": 5000,
      "real_visitors": 4200,
      "bot_traffic": 800,
      "conversion_rate": 84.00,
      "created_at": "2025-06-01T00:00:00Z",
      "user_id": 1,
      "user_name": "admin"
    }
  ],
  "total": 25
}
```

### Audit Logs

#### GET /api/admin/audit/enhanced
Get enhanced audit logs with filtering.

**Query Parameters:**
- `action_type` (optional): Filter by action type (e.g., "login", "create_link")
- `limit` (optional): Number of logs to return (default: 100)

**Response:**
```json
{
  "success": true,
  "logs": [
    {
      "id": 1,
      "audit_id": "AUD-000001",
      "user": "admin",
      "user_id": 1,
      "action_type": "login",
      "description": "User logged in",
      "timestamp": "2025-10-24T10:00:00Z",
      "ip_address": "192.168.1.1",
      "status": "success",
      "details": {}
    }
  ],
  "stats": {
    "total_logs": 1000,
    "failed_actions": 50,
    "successful_actions": 950,
    "api_errors": 10
  }
}
```

### Settings

#### GET /api/admin/settings/enhanced
Get enhanced system settings including domain management.

**Response:**
```json
{
  "success": true,
  "domains": [
    {
      "id": 1,
      "domain": "example.com",
      "ip_address": "192.168.1.1",
      "ssl_status": true,
      "status": "active",
      "severity": "normal",
      "created_at": "2025-01-01T00:00:00Z"
    }
  ],
  "system_stats": {
    "database": {
      "type": "PostgreSQL",
      "status": "connected",
      "size": "N/A"
    },
    "email_smtp": {
      "host": "smtp.gmail.com",
      "port": "587",
      "status": "configured"
    },
    "telegram": {
      "bot_configured": true,
      "status": "active"
    },
    "payment": {
      "stripe": {
        "configured": true,
        "mode": "test"
      },
      "crypto": {
        "configured": true,
        "enabled": true
      }
    }
  }
}
```

## Metrics Consistency

### GET /api/admin/dashboard/stats/consistent
Get consistent dashboard statistics.

### GET /api/links/stats/consistent
Get consistent link statistics for current user.

Both endpoints use the same calculation method to ensure metrics match across all views.

## React Hooks

### useConsistentMetrics()
Custom hook for fetching consistent metrics in user components.

```javascript
import { useConsistentMetrics } from '@/hooks/useConsistentMetrics'

function MyComponent() {
  const {
    totalClicks,
    realVisitors,
    botsBlocked,
    activeLinks,
    loading,
    error,
    refresh
  } = useConsistentMetrics(30000) // Refresh every 30 seconds

  // Use the metrics...
}
```

### useAdminMetrics()
Custom hook for fetching admin dashboard metrics.

```javascript
import { useAdminMetrics } from '@/hooks/useConsistentMetrics'

function AdminDashboard() {
  const {
    users,
    links,
    traffic,
    campaigns,
    security,
    loading,
    error,
    refresh
  } = useAdminMetrics(30000)

  // Use the metrics...
}
```

## Components

### EnhancedTable
Reusable table component for admin panels.

```javascript
import { EnhancedTable } from '@/components/EnhancedTable'

const columns = [
  { header: 'Username', accessor: 'username' },
  {
    header: 'Status',
    accessor: 'status',
    render: (value) => <StatusBadge status={value} />
  },
]

<EnhancedTable
  columns={columns}
  data={users}
  onRowClick={(row) => console.log(row)}
  loading={false}
/>
```

### StatusBadge
Badge component for displaying status.

### RoleBadge
Badge component for displaying user roles.
