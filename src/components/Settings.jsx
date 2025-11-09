import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Label } from './ui/label'
import { Switch } from './ui/switch'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'
import { Alert, AlertDescription } from './ui/alert'
import { CreditCard, MessageSquare, Settings as SettingsIcon, Shield, CheckCircle, AlertCircle, Loader, Eye, EyeOff, Wallet, Copy, Key, Slack, Image as ImageIcon, DollarSign, Calendar } from 'lucide-react'
import { toast } from 'sonner'
import APIKeyManager from './APIKeyManager'
import StripePaymentForm from './StripePaymentForm'
import CryptoPaymentForm from './CryptoPaymentForm'

const Settings = () => {
  const [user, setUser] = useState(null)
  const [activeTab, setActiveTab] = useState('api-keys')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)
  const [showPaymentForm, setShowPaymentForm] = useState(false)
  const [selectedPlan, setSelectedPlan] = useState(null)
  const [adminPaymentConfig, setAdminPaymentConfig] = useState(null)

  // User Payment/Notification Settings
  const [userSettings, setUserSettings] = useState({
    preferred_payment_method: 'card',
    telegram_personal_chat_id: '',
    telegram_personal_notifications_enabled: false,
    slack_webhook_url: '',
    slack_notifications_enabled: false,
    cdn_enabled: false,
    cdn_url: '',
    cdn_provider: 'cloudflare'
  })

  // Admin System Settings
  const [adminSystemConfig, setAdminSystemConfig] = useState({
    stripe_enabled: false,
    stripe_publishable_key: '',
    stripe_secret_key: '',
    stripe_webhook_secret: '',
    stripe_price_id: '',
    crypto_enabled: false,
    crypto_bitcoin_address: '',
    crypto_ethereum_address: '',
    telegram_system_token: '',
    telegram_system_chat_id: '',
    telegram_system_notifications_enabled: false,
    max_links_per_user: 100,
    max_campaigns_per_user: 50,
    enable_email_capture: true,
    enable_analytics: true,
    retention_days: 90,
    enable_custom_domains: true,
    maintenance_mode: false,
    enable_registrations: true
  })

  // Updated pricing plans
  const pricingPlans = [
    {
      id: 'weekly',
      name: 'Weekly',
      price: 35,
      period: 'week',
      description: 'Perfect for short-term needs',
      features: ['Advanced tracking', 'Unlimited links', '30 days retention', 'Email support']
    },
    {
      id: 'biweekly',
      name: 'Biweekly',
      price: 68,
      period: '2 weeks',
      description: 'Great for bi-weekly campaigns',
      features: ['Everything in Weekly', '60 days retention', 'Custom domains', 'Priority support']
    },
    {
      id: 'monthly',
      name: 'Monthly',
      price: 150,
      period: 'month',
      description: 'Most popular choice',
      popular: true,
      features: ['Everything in Biweekly', '90 days retention', 'API access', 'Priority support']
    },
    {
      id: 'quarterly',
      name: 'Quarterly',
      price: 420,
      period: '3 months',
      description: 'Best value for long-term',
      optional: true,
      features: ['Everything in Monthly', 'White label', 'Custom integrations', 'Dedicated support', '180 days retention']
    }
  ]

  useEffect(() => {
    fetchUserAndSettings()
  }, [])

  const fetchUserAndSettings = async () => {
    try {
      setLoading(true)
      setError(null)

      const userRes = await fetch('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (userRes.ok) {
        const userData = await userRes.json()
        setUser(userData.user)
      }

      try {
        const userSettingsRes = await fetch('/api/settings/user', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        if (userSettingsRes.ok) {
          const data = await userSettingsRes.json()
          setUserSettings(prev => ({ ...prev, ...data }))
        }
      } catch (e) {
        console.error('Error fetching user settings:', e)
      }

      try {
        const adminRes = await fetch('/api/admin/system-config', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        if (adminRes.ok) {
          const data = await adminRes.json()
          setAdminSystemConfig(prev => ({ ...prev, ...data }))
          setAdminPaymentConfig(data)
        }
      } catch (e) {
        console.error('Error fetching admin system config:', e)
      }
    } catch (error) {
      console.error('Error fetching settings:', error)
      setError('Failed to load settings')
    } finally {
      setLoading(false)
    }
  }

  const saveUserSettings = async () => {
    try {
      setSaving(true)
      const response = await fetch('/api/settings/user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(userSettings)
      })

      if (!response.ok) throw new Error('Failed to save user settings')
      
      toast.success('User settings saved successfully')
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (e) {
      toast.error(e.message || 'Error saving user settings')
      setError(e.message || 'Error saving user settings')
    } finally {
      setSaving(false)
    }
  }

  const saveAdminSystemConfig = async () => {
    try {
      setSaving(true)
      const response = await fetch('/api/admin/system-config', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(adminSystemConfig)
      })

      if (!response.ok) throw new Error('Failed to save admin system config')
      
      toast.success('Admin system configuration saved successfully')
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (e) {
      toast.error(e.message || 'Error saving admin system config')
      setError(e.message || 'Error saving admin system config')
    } finally {
      setSaving(false)
    }
  }

  const handlePaymentSuccess = () => {
    setShowPaymentForm(false)
    setSelectedPlan(null)
    toast.success('Subscription process initiated. Check your email for confirmation.')
    // Optionally, refresh user data
    fetchUserAndSettings()
  }

  const handlePaymentCancel = () => {
    setShowPaymentForm(false)
    setSelectedPlan(null)
    toast.info('Payment cancelled.')
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full">
        <Loader className="h-8 w-8 animate-spin text-blue-500" />
        <span className="ml-2 text-white">Loading Settings...</span>
      </div>
    )
  }

  if (error && !success) {
    return (
      <Alert variant="destructive" className="bg-red-900/20 border-red-700">
        <AlertCircle className="h-4 w-4 text-red-500" />
        <AlertDescription className="text-red-400">{error}</AlertDescription>
      </Alert>
    )
  }

  const isAdmin = user?.role === 'main_admin' || user?.role === 'admin'

  return (
    <div className="space-y-6 p-6">
      <h1 className="text-3xl font-bold text-white">Settings</h1>
      <p className="text-slate-400">Manage your account preferences, API keys, and system configurations.</p>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3 md:grid-cols-5 h-auto bg-slate-800 border border-slate-700">
          <TabsTrigger value="api-keys" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white text-slate-300">
            <Key className="h-4 w-4 mr-2" /> API Keys
          </TabsTrigger>
          <TabsTrigger value="notifications" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white text-slate-300">
            <MessageSquare className="h-4 w-4 mr-2" /> Notifications
          </TabsTrigger>
          <TabsTrigger value="payments" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white text-slate-300">
            <CreditCard className="h-4 w-4 mr-2" /> Payments
          </TabsTrigger>
          <TabsTrigger value="cdn" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white text-slate-300">
            <ImageIcon className="h-4 w-4 mr-2" /> CDN
          </TabsTrigger>
          {isAdmin && (
            <TabsTrigger value="system" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white text-slate-300">
              <SettingsIcon className="h-4 w-4 mr-2" /> System Config
            </TabsTrigger>
          )}
        </TabsList>

        {/* API Keys Tab */}
        <TabsContent value="api-keys" className="mt-4">
          <APIKeyManager />
        </TabsContent>

        {/* Notifications Tab */}
        <TabsContent value="notifications" className="mt-4">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">Notification Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Telegram Notifications */}
              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-blue-400 flex items-center">
                  <MessageSquare className="h-5 w-5 mr-2" /> Telegram Notifications
                </h3>
                <div className="flex items-center justify-between">
                  <Label htmlFor="telegram-switch" className="text-slate-300">
                    Enable Personal Telegram Notifications
                  </Label>
                  <Switch
                    id="telegram-switch"
                    checked={userSettings.telegram_personal_notifications_enabled}
                    onCheckedChange={(checked) => setUserSettings(prev => ({ ...prev, telegram_personal_notifications_enabled: checked }))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="telegram-chat-id" className="text-slate-300">
                    Personal Telegram Chat ID
                  </Label>
                  <Input
                    id="telegram-chat-id"
                    type="text"
                    placeholder="Your Telegram Chat ID"
                    value={userSettings.telegram_personal_chat_id}
                    onChange={(e) => setUserSettings(prev => ({ ...prev, telegram_personal_chat_id: e.target.value }))}
                    className="bg-slate-700 border-slate-600 text-white"
                  />
                  <p className="text-xs text-slate-500">
                    Find your chat ID by messaging your bot and checking the update object.
                  </p>
                </div>
              </div>

              {/* Slack Notifications */}
              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-blue-400 flex items-center">
                  <Slack className="h-5 w-5 mr-2" /> Slack Notifications
                </h3>
                <div className="flex items-center justify-between">
                  <Label htmlFor="slack-switch" className="text-slate-300">
                    Enable Slack Notifications
                  </Label>
                  <Switch
                    id="slack-switch"
                    checked={userSettings.slack_notifications_enabled}
                    onCheckedChange={(checked) => setUserSettings(prev => ({ ...prev, slack_notifications_enabled: checked }))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="slack-webhook" className="text-slate-300">
                    Slack Webhook URL
                  </Label>
                  <Input
                    id="slack-webhook"
                    type="text"
                    placeholder="https://hooks.slack.com/services/..."
                    value={userSettings.slack_webhook_url}
                    onChange={(e) => setUserSettings(prev => ({ ...prev, slack_webhook_url: e.target.value }))}
                    className="bg-slate-700 border-slate-600 text-white"
                  />
                  <p className="text-xs text-slate-500">
                    Create an incoming webhook in your Slack workspace settings.
                  </p>
                </div>
              </div>

              <Button onClick={saveUserSettings} disabled={saving} className="w-full bg-blue-600 hover:bg-blue-700 text-white">
                {saving ? <Loader className="mr-2 h-4 w-4 animate-spin" /> : <CheckCircle className="mr-2 h-4 w-4" />}
                {saving ? 'Saving...' : 'Save Notification Settings'}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Payments Tab */}
        <TabsContent value="payments" className="mt-4">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <DollarSign className="h-5 w-5 text-green-400" /> Subscription & Payment
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {user?.plan_type && (
                <Alert className="bg-green-900/20 border-green-700">
                  <Calendar className="h-4 w-4 text-green-500" />
                  <AlertDescription className="text-green-400">
                    You are currently on the <span className="font-bold">{user.plan_type.toUpperCase()}</span> plan.
                    {user.subscription_expiry && (
                      <span> Your subscription expires on <span className="font-bold">{new Date(user.subscription_expiry).toLocaleDateString()}</span>.</span>
                    )}
                  </AlertDescription>
                </Alert>
              )}

              {showPaymentForm && selectedPlan ? (
                <div className="space-y-4">
                  <h3 className="text-xl font-semibold text-white">Payment for {selectedPlan.name} Plan (${selectedPlan.price})</h3>
                  <div className="space-y-4">
                    <div className="flex items-center space-x-4">
                      <Label htmlFor="payment-method-card" className="flex items-center space-x-2 text-white">
                        <Input
                          id="payment-method-card"
                          type="radio"
                          name="payment-method"
                          value="card"
                          checked={userSettings.preferred_payment_method === 'card'}
                          onChange={() => setUserSettings(prev => ({ ...prev, preferred_payment_method: 'card' }))}
                          className="form-radio text-blue-600 bg-slate-700 border-slate-600"
                        />
                        <CreditCard className="h-5 w-5 text-blue-400" />
                        <span>Card (Stripe)</span>
                      </Label>
                      <Label htmlFor="payment-method-crypto" className="flex items-center space-x-2 text-white">
                        <Input
                          id="payment-method-crypto"
                          type="radio"
                          name="payment-method"
                          value="crypto"
                          checked={userSettings.preferred_payment_method === 'crypto'}
                          onChange={() => setUserSettings(prev => ({ ...prev, preferred_payment_method: 'crypto' }))}
                          className="form-radio text-orange-600 bg-slate-700 border-slate-600"
                        />
                        <Wallet className="h-5 w-5 text-orange-400" />
                        <span>Crypto</span>
                      </Label>
                    </div>

                    {userSettings.preferred_payment_method === 'card' && adminPaymentConfig?.stripe_enabled && (
                      <StripePaymentForm 
                        planType={selectedPlan.id} 
                        onSuccess={handlePaymentSuccess} 
                        onCancel={handlePaymentCancel} 
                      />
                    )}
                    {userSettings.preferred_payment_method === 'crypto' && adminPaymentConfig?.crypto_enabled && (
                      <CryptoPaymentForm 
                        planType={selectedPlan.id} 
                        planPrice={selectedPlan.price}
                        onSuccess={handlePaymentSuccess} 
                        onCancel={handlePaymentCancel} 
                      />
                    )}
                    {userSettings.preferred_payment_method === 'card' && !adminPaymentConfig?.stripe_enabled && (
                      <Alert variant="destructive" className="bg-red-900/20 border-red-700">
                        <AlertCircle className="h-4 w-4 text-red-500" />
                        <AlertDescription className="text-red-400">Stripe payment is currently disabled by the administrator.</AlertDescription>
                      </Alert>
                    )}
                    {userSettings.preferred_payment_method === 'crypto' && !adminPaymentConfig?.crypto_enabled && (
                      <Alert variant="destructive" className="bg-red-900/20 border-red-700">
                        <AlertCircle className="h-4 w-4 text-red-500" />
                        <AlertDescription className="text-red-400">Crypto payment is currently disabled by the administrator.</AlertDescription>
                      </Alert>
                    )}
                  </div>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {pricingPlans.map((plan) => (
                    <Card 
                      key={plan.id} 
                      className={`bg-slate-700 border-2 ${plan.popular ? 'border-blue-500' : 'border-slate-600'} hover:border-blue-400 transition-all`}
                    >
                      <CardHeader className="pb-4">
                        <CardTitle className="text-white text-xl flex justify-between items-center">
                          {plan.name}
                          {plan.popular && <span className="text-xs font-semibold px-2 py-1 rounded-full bg-blue-500 text-white">Popular</span>}
                        </CardTitle>
                        <p className="text-slate-300 text-3xl font-bold">${plan.price} <span className="text-sm font-normal text-slate-400">/{plan.period}</span></p>
                        <p className="text-sm text-slate-400">{plan.description}</p>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <ul className="space-y-2 text-slate-300">
                          {plan.features.map((feature, index) => (
                            <li key={index} className="flex items-center text-sm">
                              <CheckCircle className="h-4 w-4 mr-2 text-green-400" /> {feature}
                            </li>
                          ))}
                        </ul>
                        <Button 
                          onClick={() => {
                            setSelectedPlan(plan)
                            setShowPaymentForm(true)
                          }}
                          className="w-full bg-green-600 hover:bg-green-700 text-white"
                          disabled={user?.plan_type === plan.id}
                        >
                          {user?.plan_type === plan.id ? 'Current Plan' : 'Select Plan'}
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* CDN Tab */}
        <TabsContent value="cdn" className="mt-4">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">CDN Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-blue-400 flex items-center">
                  <ImageIcon className="h-5 w-5 mr-2" /> Content Delivery Network
                </h3>
                <div className="flex items-center justify-between">
                  <Label htmlFor="cdn-switch" className="text-slate-300">
                    Enable CDN for Assets
                  </Label>
                  <Switch
                    id="cdn-switch"
                    checked={userSettings.cdn_enabled}
                    onCheckedChange={(checked) => setUserSettings(prev => ({ ...prev, cdn_enabled: checked }))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="cdn-url" className="text-slate-300">
                    CDN Base URL
                  </Label>
                  <Input
                    id="cdn-url"
                    type="url"
                    placeholder="https://cdn.example.com"
                    value={userSettings.cdn_url}
                    onChange={(e) => setUserSettings(prev => ({ ...prev, cdn_url: e.target.value }))}
                    className="bg-slate-700 border-slate-600 text-white"
                  />
                  <p className="text-xs text-slate-500">
                    The base URL where your static assets are hosted.
                  </p>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="cdn-provider" className="text-slate-300">
                    CDN Provider
                  </Label>
                  <Input
                    id="cdn-provider"
                    type="text"
                    placeholder="cloudflare"
                    value={userSettings.cdn_provider}
                    onChange={(e) => setUserSettings(prev => ({ ...prev, cdn_provider: e.target.value }))}
                    className="bg-slate-700 border-slate-600 text-white"
                  />
                  <p className="text-xs text-slate-500">
                    e.g., cloudflare, aws, custom
                  </p>
                </div>
              </div>

              <Button onClick={saveUserSettings} disabled={saving} className="w-full bg-blue-600 hover:bg-blue-700 text-white">
                {saving ? <Loader className="mr-2 h-4 w-4 animate-spin" /> : <CheckCircle className="mr-2 h-4 w-4" />}
                {saving ? 'Saving...' : 'Save CDN Settings'}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* System Config Tab (Admin Only) */}
        {isAdmin && (
          <TabsContent value="system" className="mt-4">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">System Configuration (Admin)</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* General Settings */}
                <div className="space-y-4">
                  <h3 className="text-xl font-semibold text-red-400 flex items-center">
                    <SettingsIcon className="h-5 w-5 mr-2" /> General System Settings
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="maintenance-mode" className="text-slate-300">
                        Maintenance Mode
                      </Label>
                      <Switch
                        id="maintenance-mode"
                        checked={adminSystemConfig.maintenance_mode}
                        onCheckedChange={(checked) => setAdminSystemConfig(prev => ({ ...prev, maintenance_mode: checked }))}
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label htmlFor="enable-registrations" className="text-slate-300">
                        Enable New Registrations
                      </Label>
                      <Switch
                        id="enable-registrations"
                        checked={adminSystemConfig.enable_registrations}
                        onCheckedChange={(checked) => setAdminSystemConfig(prev => ({ ...prev, enable_registrations: checked }))}
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label htmlFor="enable-email-capture" className="text-slate-300">
                        Enable Email Capture
                      </Label>
                      <Switch
                        id="enable-email-capture"
                        checked={adminSystemConfig.enable_email_capture}
                        onCheckedChange={(checked) => setAdminSystemConfig(prev => ({ ...prev, enable_email_capture: checked }))}
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label htmlFor="enable-analytics" className="text-slate-300">
                        Enable Analytics Tracking
                      </Label>
                      <Switch
                        id="enable-analytics"
                        checked={adminSystemConfig.enable_analytics}
                        onCheckedChange={(checked) => setAdminSystemConfig(prev => ({ ...prev, enable_analytics: checked }))}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="retention-days" className="text-slate-300">
                        Data Retention Days
                      </Label>
                      <Input
                        id="retention-days"
                        type="number"
                        placeholder="90"
                        value={adminSystemConfig.retention_days}
                        onChange={(e) => setAdminSystemConfig(prev => ({ ...prev, retention_days: parseInt(e.target.value) || 0 }))}
                        className="bg-slate-700 border-slate-600 text-white"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="max-links" className="text-slate-300">
                        Max Links Per User
                      </Label>
                      <Input
                        id="max-links"
                        type="number"
                        placeholder="100"
                        value={adminSystemConfig.max_links_per_user}
                        onChange={(e) => setAdminSystemConfig(prev => ({ ...prev, max_links_per_user: parseInt(e.target.value) || 0 }))}
                        className="bg-slate-700 border-slate-600 text-white"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="max-campaigns" className="text-slate-300">
                        Max Campaigns Per User
                      </Label>
                      <Input
                        id="max-campaigns"
                        type="number"
                        placeholder="50"
                        value={adminSystemConfig.max_campaigns_per_user}
                        onChange={(e) => setAdminSystemConfig(prev => ({ ...prev, max_campaigns_per_user: parseInt(e.target.value) || 0 }))}
                        className="bg-slate-700 border-slate-600 text-white"
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label htmlFor="enable-custom-domains" className="text-slate-300">
                        Enable Custom Domains
                      </Label>
                      <Switch
                        id="enable-custom-domains"
                        checked={adminSystemConfig.enable_custom_domains}
                        onCheckedChange={(checked) => setAdminSystemConfig(prev => ({ ...prev, enable_custom_domains: checked }))}
                      />
                    </div>
                  </div>
                </div>

                {/* Payment Settings */}
                <div className="space-y-4">
                  <h3 className="text-xl font-semibold text-red-400 flex items-center">
                    <DollarSign className="h-5 w-5 mr-2" /> Payment Gateway Settings
                  </h3>
                  <div className="space-y-4 border p-4 rounded-lg border-slate-700">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="stripe-enabled" className="text-slate-300">
                        Enable Stripe Payments
                      </Label>
                      <Switch
                        id="stripe-enabled"
                        checked={adminSystemConfig.stripe_enabled}
                        onCheckedChange={(checked) => setAdminSystemConfig(prev => ({ ...prev, stripe_enabled: checked }))}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="stripe-publishable-key" className="text-slate-300">
                        Stripe Publishable Key
                      </Label>
                      <Input
                        id="stripe-publishable-key"
                        type="text"
                        placeholder="pk_live_..."
                        value={adminSystemConfig.stripe_publishable_key}
                        onChange={(e) => setAdminSystemConfig(prev => ({ ...prev, stripe_publishable_key: e.target.value }))}
                        className="bg-slate-700 border-slate-600 text-white"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="stripe-secret-key" className="text-slate-300">
                        Stripe Secret Key
                      </Label>
                      <Input
                        id="stripe-secret-key"
                        type="password"
                        placeholder="sk_live_..."
                        value={adminSystemConfig.stripe_secret_key}
                        onChange={(e) => setAdminSystemConfig(prev => ({ ...prev, stripe_secret_key: e.target.value }))}
                        className="bg-slate-700 border-slate-600 text-white"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="stripe-webhook-secret" className="text-slate-300">
                        Stripe Webhook Secret
                      </Label>
                      <Input
                        id="stripe-webhook-secret"
                        type="text"
                        placeholder="whsec_..."
                        value={adminSystemConfig.stripe_webhook_secret}
                        onChange={(e) => setAdminSystemConfig(prev => ({ ...prev, stripe_webhook_secret: e.target.value }))}
                        className="bg-slate-700 border-slate-600 text-white"
                      />
                    </div>
                  </div>

                  <div className="space-y-4 border p-4 rounded-lg border-slate-700">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="crypto-enabled" className="text-slate-300">
                        Enable Crypto Payments
                      </Label>
                      <Switch
                        id="crypto-enabled"
                        checked={adminSystemConfig.crypto_enabled}
                        onCheckedChange={(checked) => setAdminSystemConfig(prev => ({ ...prev, crypto_enabled: checked }))}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="crypto-bitcoin-address" className="text-slate-300">
                        Bitcoin Wallet Address
                      </Label>
                      <Input
                        id="crypto-bitcoin-address"
                        type="text"
                        placeholder="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
                        value={adminSystemConfig.crypto_bitcoin_address}
                        onChange={(e) => setAdminSystemConfig(prev => ({ ...prev, crypto_bitcoin_address: e.target.value }))}
                        className="bg-slate-700 border-slate-600 text-white"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="crypto-ethereum-address" className="text-slate-300">
                        Ethereum Wallet Address
                      </Label>
                      <Input
                        id="crypto-ethereum-address"
                        type="text"
                        placeholder="0x..."
                        value={adminSystemConfig.crypto_ethereum_address}
                        onChange={(e) => setAdminSystemConfig(prev => ({ ...prev, crypto_ethereum_address: e.target.value }))}
                        className="bg-slate-700 border-slate-600 text-white"
                      />
                    </div>
                  </div>
                </div>

                {/* Telegram System Notifications */}
                <div className="space-y-4">
                  <h3 className="text-xl font-semibold text-red-400 flex items-center">
                    <MessageSquare className="h-5 w-5 mr-2" /> System Telegram Notifications
                  </h3>
                  <div className="flex items-center justify-between">
                    <Label htmlFor="system-telegram-switch" className="text-slate-300">
                      Enable System Telegram Notifications
                    </Label>
                    <Switch
                      id="system-telegram-switch"
                      checked={adminSystemConfig.telegram_system_notifications_enabled}
                      onCheckedChange={(checked) => setAdminSystemConfig(prev => ({ ...prev, telegram_system_notifications_enabled: checked }))}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="system-telegram-token" className="text-slate-300">
                      Telegram Bot Token
                    </Label>
                    <Input
                      id="system-telegram-token"
                      type="text"
                      placeholder="123456:ABC-DEF1234ghIkl-jkl_mnoP"
                      value={adminSystemConfig.telegram_system_token}
                      onChange={(e) => setAdminSystemConfig(prev => ({ ...prev, telegram_system_token: e.target.value }))}
                      className="bg-slate-700 border-slate-600 text-white"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="system-telegram-chat-id" className="text-slate-300">
                      System Telegram Chat ID
                    </Label>
                    <Input
                      id="system-telegram-chat-id"
                      type="text"
                      placeholder="-1001234567890"
                      value={adminSystemConfig.telegram_system_chat_id}
                      onChange={(e) => setAdminSystemConfig(prev => ({ ...prev, telegram_system_chat_id: e.target.value }))}
                      className="bg-slate-700 border-slate-600 text-white"
                    />
                    <p className="text-xs text-slate-500">
                      This is usually a group or channel ID for system alerts.
                    </p>
                  </div>
                </div>

                <Button onClick={saveAdminSystemConfig} disabled={saving} className="w-full bg-red-600 hover:bg-red-700 text-white">
                  {saving ? <Loader className="mr-2 h-4 w-4 animate-spin" /> : <CheckCircle className="mr-2 h-4 w-4" />}
                  {saving ? 'Saving...' : 'Save System Configuration'}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        )}
      </Tabs>
    </div>
  )
}

export default Settings
