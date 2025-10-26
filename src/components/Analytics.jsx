import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select'
import { Badge } from './ui/badge'
import { Progress } from './ui/progress'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  AreaChart,
  Area
} from 'recharts'
import { 
  TrendingUp, 
  Users, 
  MousePointer, 
  Mail, 
  Globe, 
  Smartphone, 
  Monitor, 
  Tablet,
  RefreshCw,
  Download,
  Calendar,
  Target,
  Eye,
  BarChart3,
  Activity,
  Clock
} from 'lucide-react'

const Analytics = () => {
  const [timeRange, setTimeRange] = useState('7')
  const [loading, setLoading] = useState(true)
  const [analytics, setAnalytics] = useState({
    totalClicks: 0,
    uniqueVisitors: 0,
    conversionRate: 0,
    bounceRate: 0,
    capturedEmails: 0,
    activeLinks: 0,
    avgSessionDuration: 0
  })
  const [topCampaigns, setTopCampaigns] = useState([])
  const [devices, setDevices] = useState([])
  const [countries, setCountries] = useState([])
  const [performanceData, setPerformanceData] = useState([])



  useEffect(() => {
    fetchAnalyticsData()
  }, [timeRange])

  const handleRefresh = () => {
    fetchAnalyticsData()
  }

  const handleExport = () => {
    // Export analytics data as CSV
    const csvData = [
      ['Metric', 'Value'],
      ['Total Clicks', analytics.totalClicks],
      ['Unique Visitors', analytics.uniqueVisitors],
      ['Conversion Rate', `${analytics.conversionRate}%`],
      ['Bounce Rate', `${analytics.bounceRate}%`],
      ['Captured Emails', analytics.capturedEmails],
      ['Active Links', analytics.activeLinks],
      ['Avg Session Duration', `${analytics.avgSessionDuration}m`]
    ]
    
    const csvContent = csvData.map(row => row.join(',')).join('\n')
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `analytics-${new Date().toISOString().split('T')[0]}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  }

  const fetchAnalyticsData = async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/analytics/overview?period=${timeRange}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setAnalytics({
          totalClicks: data.totalClicks || 0,
          uniqueVisitors: data.uniqueVisitors || 0,
          conversionRate: data.conversionRate || 0,
          bounceRate: data.bounceRate || 0,
          capturedEmails: data.capturedEmails || 0,
          activeLinks: data.activeLinks || 0,
          avgSessionDuration: data.avgSessionDuration || 0
        })
        setTopCampaigns(data.topCampaigns || [])
        setCountries(data.countries || [])
        setDevices(data.devices || [])
        setPerformanceData(data.performanceData || [])
      } else {
        console.error('Failed to fetch analytics data')
        // Optionally, set analytics to default/empty states on failure
        setAnalytics({
          totalClicks: 0,
          uniqueVisitors: 0,
          conversionRate: 0,
          bounceRate: 0,
          capturedEmails: 0,
          activeLinks: 0,
          avgSessionDuration: 0
        })
        setTopCampaigns([])
        setCountries([])
        setDevices([])
        setPerformanceData([])
      }
    } catch (error) {
      console.error('Error fetching analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Advanced Analytics</h1>
        <p className="text-muted-foreground">Detailed performance insights and metrics</p>
      </div>

      {/* Controls */}
      <div className="flex flex-col sm:flex-row gap-4 mb-8">
        <Select value={timeRange} onValueChange={setTimeRange}>
          <SelectTrigger className="w-full sm:w-[180px] bg-slate-800 border-slate-700 text-white">
            <SelectValue placeholder="Select time range" />
          </SelectTrigger>
          <SelectContent className="bg-slate-800 border-slate-700">
            <SelectItem value="1">Last 24 hours</SelectItem>
            <SelectItem value="7">Last 7 days</SelectItem>
            <SelectItem value="30">Last 30 days</SelectItem>
            <SelectItem value="90">Last 90 days</SelectItem>
          </SelectContent>
        </Select>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={handleRefresh} className="border-slate-600 text-slate-300 hover:bg-slate-700">
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button variant="outline" size="sm" onClick={handleExport} className="border-slate-600 text-slate-300 hover:bg-slate-700">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* Analytics Metric Cards - 3-Grid Layout - Mobile Responsive */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        <Card className="hover:shadow-md transition-all cursor-pointer bg-card/50 border-border/50">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1">Total Clicks</p>
                <p className="text-2xl font-bold text-foreground">{analytics.totalClicks.toLocaleString()}</p>
                <p className="text-xs text-green-400 mt-1">+12% from last period</p>
              </div>
              <div className="p-2 bg-blue-500/20 rounded-full">
                <MousePointer className="h-5 w-5 text-blue-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-all cursor-pointer bg-card/50 border-border/50">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
              <p className="text-xs font-medium text-muted-foreground mb-1">Unique Visitors</p>
                <p className="text-2xl font-bold text-foreground">{analytics.uniqueVisitors.toLocaleString()}</p>
                <p className="text-xs text-green-400 mt-1">+8% from last period</p>
              </div>
              <div className="p-2 bg-green-500/20 rounded-full">
                <Users className="h-5 w-5 text-green-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-all cursor-pointer bg-card/50 border-border/50">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1">Conversion Rate</p>
                <p className="text-2xl font-bold text-foreground">{analytics.conversionRate}%</p>
                <p className="text-xs text-green-400 mt-1">+2.3% from last period</p>
              </div>
              <div className="p-2 bg-purple-500/20 rounded-full">
                <TrendingUp className="h-5 w-5 text-purple-400" />
              </div>
            </div>
          </CardContent>
        </Card>
        </div>

      {/* Compact Metric Cards - 7 cards in one row - Mobile: 2 cols, Tablet: 4 cols, Desktop: 7 cols */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-3 mb-6">
        <Card className="hover:shadow-md transition-all cursor-pointer bg-card/50 border-border/50">
          <CardContent className="p-3">
            <div className="flex items-center justify-between">
              <div>
              <p className="text-xs font-medium text-muted-foreground mb-1">Total Clicks</p>
                <div className="text-xl font-bold text-foreground">{analytics.totalClicks.toLocaleString()}</div>
              </div>
              <MousePointer className="h-4 w-4 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-all cursor-pointer bg-card/50 border-border/50">
          <CardContent className="p-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1">Unique Visitors</p>
                <div className="text-xl font-bold text-foreground">{analytics.uniqueVisitors.toLocaleString()}</div>
              </div>
              <Users className="h-4 w-4 text-green-500" />
	            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-all cursor-pointer bg-card/50 border-border/50">
          <CardContent className="p-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1">Conversion Rate</p>               <div className="text-xl font-bold text-foreground">{analytics.conversionRate}%</div>
              </div>
              <Target className="h-4 w-4 text-purple-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-all cursor-pointer bg-card/50 border-border/50">
          <CardContent className="p-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1">Bounce Rate</p>
                <div className="text-xl font-bold text-foreground">{analytics.bounceRate}%</div>
              </div>
              <Activity className="h-4 w-4 text-orange-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-all cursor-pointer bg-card/50 border-border/50">
          <CardContent className="p-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1">Captured Emails</p>
                <div className="text-xl font-bold text-foreground">{analytics.capturedEmails}</div>
              </div>
              <Mail className="h-4 w-4 text-teal-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-all cursor-pointer bg-card/50 border-border/50">
          <CardContent className="p-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1">Active Links</p>
                <div className="text-xl font-bold text-foreground">{analytics.activeLinks}</div>
              </div>
              <TrendingUp className="h-4 w-4 text-indigo-500" />
            </div>
          </CardContent>
        </Card>

        <<Card className="hover:shadow-md transition-all cursor-pointer bg-card/50 border-border/50">
          <CardContent className="p-3">
            <div className="flex items-center justify-between">
              <div>
             <p className="text-xs font-medium text-muted-foreground mb-1">Avg. Session Duration</p>         <div className="text-xl font-bold text-foreground">{analytics.avgSessionDuration}m</div>
              </div>
            <Clock className="h-4 w-4 text-yellow-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Grid - Side by Side (2 columns) - Mobile: 1 col, Desktop: 2 cols */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        {/* Performance Over Time Chart */}
        <Card className="bg-card border-border hover:shadow-md transition-all">
          <CardHeader className="pb-2">
            <CardTitle className="text-base font-semibold text-foreground">Performance Trends</CardTitle>
            <p className="text-xs text-muted-foreground">Clicks, visitors, and conversions over time</div>
          </CardHeader>
          <CardContent className="p-4">
            <ResponsiveContainer width="100%" height={280}>
              <AreaChart data={performanceData}>
                <defs>
                  <linearGradient id="colorClicks" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1}/>
                  </linearGradient>
                  <linearGradient id="colorVisitors" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0.1}/>
                  </linearGradient>
                  <linearGradient id="colorConversions" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#f59e0b" stopOpacity={0.1}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                <XAxis 
                  dataKey="date" 
                  fontSize={10}
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={(value) => value.split('-')[2]}
                />
                <YAxis 
                  fontSize={10}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'hsl(var(--background))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '6px',
                    fontSize: '12px'
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="clicks"
                  stroke="#3b82f6"
                  fillOpacity={1}
                  fill="url(#colorClicks)"
                />
                <Area
                  type="monotone"
                  dataKey="visitors"
                  stroke="#10b981"
                  fillOpacity={1}
                  fill="url(#colorVisitors)"
                />
                <Area
                  type="monotone"
                  dataKey="conversions"
                  stroke="#f59e0b"
                  fillOpacity={1}
                  fill="url(#colorConversions)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Device Breakdown Chart */}
        <Card className="bg-card border-border hover:shadow-md transition-all">
          <CardHeader className="pb-2">
            <CardTitle className="text-base font-semibold text-foreground">Device Distribution</CardTitle>
            <p className="text-xs text-muted-foreground">Traffic breakdown by device type</div>
          </CardHeader>
          <CardContent className="p-4">
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={devices}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={100}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {devices.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value, name) => [value.toLocaleString(), name]}
                  contentStyle={{
                    backgroundColor: 'hsl(var(--background))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '6px',
                    fontSize: '12px'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="flex justify-center gap-4 mt-2">
              {devices.map((item, index) => (
                <div key={index} className="flex items-center gap-2">
                  <div 
                    className="w-3 h-3 rounded-full" 
                    style={{ backgroundColor: item.color }}
                  ></div>
                  <span className="text-xs text-muted-foreground">
                    {item.name} {item.percentage}%
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Geographic Distribution Chart */}
        <Card className="bg-card border-border hover:shadow-md transition-all">
          <CardHeader className="pb-2">
            <CardTitle className="text-base font-semibold text-foreground">Geographic Distribution</CardTitle>
            <p className="text-xs text-muted-foreground">Top countries by traffic volume</div>
          </CardHeader>
          <CardContent className="p-4">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={countries.slice(0, 5)} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                <XAxis 
                  type="number"
                  fontSize={10}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis 
                  type="category"
                  dataKey="name"
                  fontSize={10}
                  tickLine={false}
                  axisLine={false}
                  width={80}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'hsl(var(--background))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '6px',
                    fontSize: '12px'
                  }}
                />
                <Bar dataKey="clicks" fill="#3b82f6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Campaign Performance Chart */}
        <Card className="bg-card border-border hover:shadow-md transition-all">
          <CardHeader className="pb-2">
            <CardTitle className="text-base font-semibold text-foreground">Campaign Performance</CardTitle>
            <p className="text-xs text-muted-foreground">Top performing campaigns by conversion rate</p>
          </CardHeader>
          <CardContent className="p-4">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={topCampaigns.slice(0, 5)}>
                <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                <XAxis 
                  dataKey="name" 
                  fontSize={10}
                  tickLine={false}
                  axisLine={false}
                  angle={-45}
                  textAnchor="end"
                  height={60}
                />
                <YAxis 
                  fontSize={10}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'hsl(var(--background))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '6px',
                    fontSize: '12px'
                  }}
                />
                <Bar dataKey="rate" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Tables - Mobile: 1 col, Desktop: 2 cols */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Top Countries Table */}
        <Card className="bg-card border-border hover:shadow-md transition-all">
          <CardHeader>
            <CardTitle className="text-base font-semibold text-foreground">Top Countries</CardTitle>
            <CardDescription className="text-muted-foreground">Traffic distribution by country</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {countries.slice(0, 6).map((country, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-lg">{country.flag}</span>
                    <div>
                      <p className="font-medium text-sm text-foreground">{country.name}</p>
                      <p className="text-xs text-muted-foreground">{country.clicks.toLocaleString()} clicks</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-sm text-foreground">{country.percentage}%</p>
                    <Progress value={country.percentage} className="w-16 h-2" />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Top Campaigns Table */}
        <Card className="bg-card border-border hover:shadow-md transition-all">
          <CardHeader>
            <CardTitle className="text-base font-semibold text-foreground">Campaign Performance</CardTitle>
            <CardDescription className="text-muted-foreground">Top performing campaigns</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {topCampaigns.slice(0, 5).map((campaign, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                      <Target className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="font-medium text-sm text-foreground">{campaign.name}</p>
<p className="text-xs text-muted-foreground">
	                        {campaign.clicks.toLocaleString()} clicks • {campaign.conversions} conversions
	                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <Badge variant={campaign.status === 'active' ? 'default' : 'secondary'}>
                      {campaign.rate}%
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Analytics

