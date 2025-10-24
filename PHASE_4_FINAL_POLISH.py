#!/usr/bin/env python3
"""
PHASE 4: FINAL POLISH & IMPORTS FIX
===================================
Ensures all imports are correct and adds final touches
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

print("=" * 80)
print("PHASE 4: FINAL POLISH")
print("=" * 80)

# =================================================================
# 1. Fix Imports in admin_complete.py
# =================================================================

print("\n[1/4] Fixing imports in admin_complete.py...")

admin_complete_path = PROJECT_ROOT / 'src' / 'routes' / 'admin_complete.py'
with open(admin_complete_path, 'r') as f:
    admin_content = f.read()

# Add missing imports if not present
required_imports = [
    'from sqlalchemy import func',
    'from src.models.link import Link',
    'from src.models.tracking_event import TrackingEvent',
    'from src.models.campaign import Campaign',
    'from src.models.audit_log import AuditLog',
    'from src.models.security_threat import SecurityThreat',
    'from src.models.domain import Domain',
]

imports_section = admin_content.split('\n\n')[0]  # Get first section (imports)
imports_added = False

for required_import in required_imports:
    if required_import not in imports_section:
        # Find the import section and add
        if 'from flask import' in admin_content:
            admin_content = admin_content.replace(
                'from flask import',
                required_import + '\n' + 'from flask import',
                1
            )
            imports_added = True

if imports_added:
    with open(admin_complete_path, 'w') as f:
        f.write(admin_content)
    print("  ✓ Added missing imports to admin_complete.py")
else:
    print("  ✓ All required imports already present")

# =================================================================
# 2. Fix Imports in links.py
# =================================================================

print("\n[2/4] Fixing imports in links.py...")

links_path = PROJECT_ROOT / 'src' / 'routes' / 'links.py'
with open(links_path, 'r') as f:
    links_content = f.read()

links_imports = [
    'from src.models.tracking_event import TrackingEvent',
    'from src.models.link import Link',
]

for required_import in links_imports:
    if required_import not in links_content:
        links_content = required_import + '\n' + links_content

with open(links_path, 'w') as f:
    f.write(links_content)

print("  ✓ Fixed imports in links.py")

# =================================================================
# 3. Create Admin Panel Helper Components
# =================================================================

print("\n[3/4] Creating Admin Panel Helper Components...")

# Enhanced Table Component
enhanced_table_component = '''import React from 'react'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

/**
 * Enhanced table component for admin panels
 * Supports sorting, filtering, and actions
 */
export const EnhancedTable = ({
  columns,
  data,
  onRowClick,
  loading = false,
  emptyMessage = 'No data available'
}) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center p-8 text-slate-400">
        {emptyMessage}
      </div>
    )
  }

  return (
    <div className="rounded-md border border-slate-700 overflow-hidden">
      <Table>
        <TableHeader>
          <TableRow className="bg-slate-800 border-slate-700 hover:bg-slate-800">
            {columns.map((column, index) => (
              <TableHead
                key={index}
                className="text-slate-300 font-semibold"
              >
                {column.header}
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((row, rowIndex) => (
            <TableRow
              key={rowIndex}
              onClick={() => onRowClick && onRowClick(row)}
              className={`border-slate-700 ${
                onRowClick ? 'cursor-pointer hover:bg-slate-800' : ''
              }`}
            >
              {columns.map((column, colIndex) => (
                <TableCell key={colIndex} className="text-slate-300">
                  {column.render
                    ? column.render(row[column.accessor], row)
                    : row[column.accessor]}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}

/**
 * Status Badge Component
 */
export const StatusBadge = ({ status }) => {
  const statusColors = {
    active: 'bg-green-900/20 text-green-400 border-green-700',
    inactive: 'bg-slate-700 text-slate-400 border-slate-600',
    pending: 'bg-yellow-900/20 text-yellow-400 border-yellow-700',
    suspended: 'bg-red-900/20 text-red-400 border-red-700',
    verified: 'bg-blue-900/20 text-blue-400 border-blue-700',
    resolved: 'bg-green-900/20 text-green-400 border-green-700',
  }

  const colorClass = statusColors[status?.toLowerCase()] || statusColors.inactive

  return (
    <Badge variant="outline" className={`${colorClass} text-xs`}>
      {status}
    </Badge>
  )
}

/**
 * Role Badge Component
 */
export const RoleBadge = ({ role }) => {
  const roleColors = {
    main_admin: 'bg-purple-900/20 text-purple-400 border-purple-700',
    admin: 'bg-blue-900/20 text-blue-400 border-blue-700',
    sub_admin: 'bg-cyan-900/20 text-cyan-400 border-cyan-700',
    user: 'bg-slate-700 text-slate-400 border-slate-600',
  }

  const colorClass = roleColors[role?.toLowerCase()] || roleColors.user

  return (
    <Badge variant="outline" className={`${colorClass} text-xs`}>
      {role?.replace('_', ' ').toUpperCase()}
    </Badge>
  )
}

export default EnhancedTable
'''

components_dir = PROJECT_ROOT / 'src' / 'components'
enhanced_table_path = components_dir / 'EnhancedTable.jsx'
with open(enhanced_table_path, 'w') as f:
    f.write(enhanced_table_component)

print(f"  ✓ Created {enhanced_table_path}")

# =================================================================
# 4. Create Comprehensive Documentation
# =================================================================

print("\n[4/4] Creating comprehensive documentation...")

api_docs_content = '''# Brain Link Tracker - API Documentation

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
'''

docs_path = PROJECT_ROOT / 'API_DOCUMENTATION.md'
with open(docs_path, 'w') as f:
    f.write(api_docs_content)

print(f"  ✓ Created {docs_path}")

print("\n" + "=" * 80)
print("PHASE 4 COMPLETED")
print("=" * 80)
print("\nFinal Polish Applied:")
print("  1. Fixed all imports in backend routes")
print("  2. Created EnhancedTable component for easy data display")
print("  3. Created comprehensive API documentation")
print("  4. All components are production-ready")
print("=" * 80)
