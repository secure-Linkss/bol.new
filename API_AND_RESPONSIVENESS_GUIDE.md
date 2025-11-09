# API Endpoints & Responsiveness Guide

## API Endpoints Reference

### Authentication Routes (`/api/auth/*`)
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/validate` - Validate token
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh token

### Admin Routes (`/api/admin/*`)
- `GET /api/admin/dashboard` - Dashboard statistics
- `GET /api/admin/users` - List all users
- `GET /api/admin/users/enhanced` - Enhanced user data
- `POST /api/admin/users` - Create user
- `GET /api/admin/users/<id>` - Get user details
- `PATCH /api/admin/users/<id>` - Update user
- `POST /api/admin/users/<id>/role` - Update user role
- `POST /api/admin/users/<id>/suspend` - Suspend user
- `POST /api/admin/users/<id>/approve` - Approve user
- `POST /api/admin/users/<id>/password` - Change password
- `POST /api/admin/users/<id>/extend-subscription` - Extend subscription
- `DELETE /api/admin/users/<id>` - Delete user

### Campaign Routes (`/api/campaigns/*`)
- `GET /api/campaigns` - List campaigns
- `POST /api/campaigns` - Create campaign
- `GET /api/campaigns/<name>` - Get campaign details
- `PATCH /api/campaigns/<name>` - Update campaign
- `DELETE /api/campaigns/<name>` - Delete campaign
- `GET /api/campaigns/<name>/links` - Get campaign links
- `GET /api/campaigns/intelligence/<name>` - Campaign intelligence
- `GET /api/campaigns/performance-predictions` - Performance predictions
- `GET /api/campaigns/optimization-recommendations` - Optimization recommendations

### Link Routes (`/api/links/*`)
- `GET /api/links` - List links
- `POST /api/links` - Create link
- `GET /api/links/<id>` - Get link details
- `PATCH /api/links/<id>` - Update link
- `DELETE /api/links/<id>` - Delete link
- `GET /api/links/<id>/analytics` - Link analytics

### Analytics Routes (`/api/analytics/*`)
- `GET /api/analytics/dashboard` - Dashboard analytics
- `GET /api/analytics/overview` - Analytics overview
- `GET /api/analytics/performance` - Performance metrics
- `GET /api/analytics/realtime` - Real-time data
- `GET /api/analytics/summary` - Summary statistics
- `GET /api/analytics/geography` - Geographic data
- `GET /api/analytics/geography/map-data` - Map data for geography

### Security Routes (`/api/security/*`)
- `GET /api/security/threats` - List threats
- `GET /api/security/advanced/threats` - Advanced threats
- `GET /api/security/advanced/dashboard` - Security dashboard
- `GET /api/security/advanced/statistics` - Security statistics
- `POST /api/security/advanced/analyze` - Analyze security
- `GET /api/security/advanced/honeypots` - Honeypot data
- `POST /api/security/advanced/config` - Configure security
- `GET /api/security/advanced/config` - Get security config
- `POST /api/security/advanced/whitelist` - Add to whitelist
- `POST /api/security/advanced/blacklist` - Add to blacklist
- `POST /api/security/advanced/unblock` - Unblock IP
- `GET /api/security/advanced/ip-reputation/<ip>` - Check IP reputation
- `POST /api/security/advanced/test` - Test security
- `GET /api/security/advanced/export` - Export security data

### Notification Routes (`/api/notifications/*`)
- `GET /api/notifications` - List notifications
- `GET /api/notifications/count` - Get notification count
- `POST /api/notifications` - Create notification
- `PATCH /api/notifications/<id>` - Update notification
- `DELETE /api/notifications/<id>` - Delete notification

### Settings Routes (`/api/settings/*`)
- `GET /api/settings` - Get settings
- `POST /api/settings` - Update settings
- `GET /api/settings/stripe` - Get Stripe config
- `POST /api/settings/stripe` - Update Stripe config
- `GET /api/settings/telegram` - Get Telegram config
- `POST /api/settings/telegram` - Update Telegram config
- `GET /api/settings/crypto` - Get Crypto config
- `POST /api/settings/crypto` - Update Crypto config

### Domain Routes (`/api/domains/*`)
- `GET /api/domains` - List domains
- `POST /api/domains` - Create domain
- `GET /api/domains/<id>` - Get domain details
- `PATCH /api/domains/<id>` - Update domain
- `DELETE /api/domains/<id>` - Delete domain
- `POST /api/domains/<id>/verify` - Verify domain

### Support Ticket Routes (`/api/support/tickets/*`)
- `GET /api/support/tickets` - List tickets
- `POST /api/support/tickets` - Create ticket
- `GET /api/support/tickets/<id>` - Get ticket details
- `PATCH /api/support/tickets/<id>` - Update ticket
- `DELETE /api/support/tickets/<id>` - Delete ticket
- `POST /api/support/tickets/<id>/comments` - Add comment

### Audit Log Routes (`/api/audit-logs/*`)
- `GET /api/audit-logs` - List audit logs
- `GET /api/audit-logs/export` - Export audit logs

### Subscription Routes (`/api/subscriptions/*`)
- `GET /api/subscriptions` - List subscriptions
- `POST /api/subscriptions/<user_id>/extend` - Extend subscription

### Profile Routes (`/api/profile/*`)
- `GET /api/profile` - Get user profile
- `PATCH /api/profile` - Update profile
- `PATCH /api/profile/password` - Change password

### Payment Routes (`/api/payments/*`)
- `POST /api/payments/process` - Process payment
- `GET /api/payments/history` - Payment history
- `POST /api/payments/verify` - Verify payment

### Crypto Payment Routes (`/api/crypto/*`)
- `POST /api/crypto/process` - Process crypto payment
- `GET /api/crypto/rates` - Get crypto rates
- `POST /api/crypto/verify` - Verify crypto payment

### Stripe Routes (`/api/stripe/*`)
- `POST /api/stripe/create-checkout` - Create checkout session
- `POST /api/stripe/webhook` - Handle webhook

### Broadcaster Routes (`/api/broadcaster/*`)
- `POST /api/broadcaster/send` - Send broadcast
- `GET /api/broadcaster/history` - Broadcast history
- `GET /api/broadcaster/stats` - Broadcast statistics

### Tracking Routes (No `/api` prefix)
- `GET /t/<short_code>` - Track click
- `GET /p/<short_code>` - Track page view
- `POST /track` - Track event

### Quantum Redirect Routes (No `/api` prefix)
- `GET /q/<path>` - Quantum redirect
- `POST /validate` - Validate redirect
- `POST /route` - Route redirect

---

## Responsive Design Patterns

### Breakpoints Used
```
sm:  640px   (mobile)
md:  768px   (tablet)
lg:  1024px  (desktop)
xl:  1280px  (large desktop)
2xl: 1536px  (extra large)
```

### Common Responsive Patterns

#### 1. **Mobile-First Navigation**
```jsx
// Mobile menu toggle
<button className="md:hidden">
  <Menu className="h-6 w-6" />
</button>

// Desktop sidebar (hidden on mobile)
<div className="hidden md:flex w-64">
  {/* Desktop navigation */}
</div>

// Mobile sidebar (fixed position)
<div className="md:hidden fixed inset-y-0 left-0 z-50">
  {/* Mobile navigation */}
</div>
```

#### 2. **Responsive Grid Layouts**
```jsx
// Grid that adapts to screen size
<div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
  {/* Cards */}
</div>

// Metric cards layout
<div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
  {/* Metric cards */}
</div>
```

#### 3. **Responsive Text Sizes**
```jsx
<h1 className="text-2xl sm:text-3xl md:text-4xl font-bold">
  Heading
</h1>

<p className="text-xs sm:text-sm md:text-base">
  Body text
</p>
```

#### 4. **Responsive Padding/Spacing**
```jsx
<div className="p-3 sm:p-4 md:p-6 lg:p-8">
  {/* Content with responsive padding */}
</div>

<div className="gap-2 sm:gap-3 md:gap-4 lg:gap-6">
  {/* Content with responsive gaps */}
</div>
```

#### 5. **Responsive Flex Direction**
```jsx
<div className="flex flex-col sm:flex-row gap-4">
  {/* Stacks on mobile, side-by-side on desktop */}
</div>
```

#### 6. **Hidden/Shown Elements**
```jsx
{/* Hidden on mobile, shown on tablet+ */}
<div className="hidden sm:block">
  Desktop content
</div>

{/* Shown on mobile, hidden on tablet+ */}
<div className="sm:hidden">
  Mobile content
</div>

{/* Hidden text, shown on larger screens */}
<span className="hidden sm:inline">Full text</span>
<span className="sm:hidden">Short</span>
```

#### 7. **Responsive Table Display**
```jsx
<table className="w-full">
  <thead>
    <tr>
      <th className="text-left">Always visible</th>
      <th className="hidden sm:table-cell">Desktop only</th>
    </tr>
  </thead>
</table>
```

#### 8. **Responsive Width**
```jsx
<div className="w-full sm:w-[180px] md:w-[250px]">
  {/* Responsive width */}
</div>
```

#### 9. **Responsive Modal/Dialog**
```jsx
<DialogContent className="w-[95vw] sm:w-full">
  {/* Takes 95% width on mobile, full width on desktop */}
</DialogContent>
```

#### 10. **Responsive Button Groups**
```jsx
<div className="flex flex-col sm:flex-row gap-2">
  <Button className="flex-1 text-xs sm:text-sm">
    Action 1
  </Button>
  <Button className="flex-1 text-xs sm:text-sm">
    Action 2
  </Button>
</div>
```

---

## Color Scheme (Existing)

### Background Colors
- `bg-slate-900` - Main background
- `bg-slate-800` - Secondary background
- `bg-slate-700` - Hover/active state

### Text Colors
- `text-white` - Primary text
- `text-slate-400` - Secondary text
- `text-slate-300` - Tertiary text

### Accent Colors
- `bg-blue-600` - Primary action
- `bg-red-600` - Danger/alerts
- `bg-green-600` - Success
- `bg-purple-600` - Premium/special

### Border Colors
- `border-slate-700` - Primary border
- `border-slate-600` - Secondary border

---

## Component Structure Best Practices

1. **Always use responsive grids** for multi-column layouts
2. **Hide/show content** based on screen size using `hidden` and responsive classes
3. **Use flex-col/flex-row** for responsive direction changes
4. **Adjust padding/gaps** at different breakpoints
5. **Scale text sizes** appropriately for readability
6. **Use full width** on mobile, constrained width on desktop
7. **Stack buttons vertically** on mobile, horizontally on desktop
8. **Optimize table display** by hiding columns on mobile

---

## Responsive Testing Checklist

- [ ] Mobile (320px - 640px)
- [ ] Tablet (641px - 1024px)
- [ ] Desktop (1025px+)
- [ ] Text readability at all sizes
- [ ] Button/input sizes appropriate for touch
- [ ] Navigation accessible on all devices
- [ ] Images scale properly
- [ ] No horizontal scrolling on mobile
- [ ] Modals/dialogs fit screen
- [ ] Forms stack properly on mobile

