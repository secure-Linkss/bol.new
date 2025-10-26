import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts';
import { CalendarDays, Link, MousePointer, Users, BarChart as BarChartIcon, Globe, Shield, TrendingUp, Eye, Mail, RefreshCw, Download, Search } from 'lucide-react';

const Dashboard = () => {
  const [period, setPeriod] = useState('7d');
  const [stats, setStats] = useState({
    totalLinks: 0,
    totalClicks: 0,
    avgClicksPerLink: 0
  });
  const [chartData, setChartData] = useState([]);
  const [topCountries, setTopCountries] = useState([]);
  const [topCampaigns, setTopCampaigns] = useState([]);
  const [recentCaptures, setRecentCaptures] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchDashboardData = async (selectedPeriod) => {
    try {
      setLoading(true);
      const response = await fetch(`/api/analytics/dashboard?period=${selectedPeriod}`);
      const data = await response.json();
      
      // Extract dashboard analytics data
      if (data) {
        const dashboardStats = {
          totalLinks: data.totalLinks || 0,
          totalClicks: data.totalClicks || 0,
          avgClicksPerLink: (data.totalClicks && data.totalLinks) ? (data.totalClicks / data.totalLinks).toFixed(1) : 0,
          realVisitors: data.realVisitors || 0,
          capturedEmails: data.capturedEmails || 0,
          activeLinks: data.activeLinks || 0,
          conversionRate: data.conversionRate || 0,
          deviceDesktop: data.deviceBreakdown?.desktop || 0,
          deviceMobile: data.deviceBreakdown?.mobile || 0,
          deviceTablet: data.deviceBreakdown?.tablet || 0,
          deviceDesktopPercent: data.deviceBreakdown?.desktop || 0,
          deviceMobilePercent: data.deviceBreakdown?.mobile || 0,
          deviceTabletPercent: data.deviceBreakdown?.tablet || 0
        };
        setStats(dashboardStats);

        setChartData(data.performanceOverTime || []);
        setTopCountries(data.topCountries || []);
        setTopCampaigns(data.campaignPerformance || []);
        setRecentCaptures(data.recentCaptures || []);
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData(period);
  }, [period]);

  const handlePeriodChange = (newPeriod) => {
    setPeriod(newPeriod);
  };

  const handleRefresh = () => {
    fetchDashboardData(period);
  };

  const handleExport = () => {
    if (chartData.length === 0) {
      alert("No data to export.");
      return;
    }

    const headers = ["Date", "Clicks", "Visitors", "Emails"];
    const csv = [headers.join(",")];

    chartData.forEach(item => {
      const row = [
        `"${item.date}"`, 
        `"${item.clicks}"`, 
        `"${item.visitors}"`, 
        `"${item.emails}"`
      ];
      csv.push(row.join(","));
    });

    const csvString = csv.join("\n");
    const blob = new Blob([csvString], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.setAttribute("download", "dashboard_performance_data.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Calculate additional stats from live data
  const additionalStats = {
    realVisitors: stats.realVisitors || 0,
    capturedEmails: stats.capturedEmails || 0,
    activeLinks: stats.activeLinks || 0,
    conversionRate: stats.conversionRate || 0,
    countries: topCountries.length || 0
  };

  // Device breakdown data - will be populated from API
  const deviceData = [
    { name: 'Desktop', value: 0, percentage: 0, color: '#8b5cf6' },
    { name: 'Mobile', value: 0, percentage: 0, color: '#06b6d4' },
    { name: 'Tablet', value: 0, percentage: 0, color: '#10b981' }
  ];

  // Performance over time data - use live data from API
  const performanceData = chartData.length > 0 ? chartData.map((item) => ({
    date: item.date,
    clicks: item.clicks || 0,
    visitors: item.visitors || 0,
    emails: item.emails || 0
  })) : [];

  // Top countries data - use live data from API
  const countriesData = topCountries.length > 0 ? topCountries : [];

  // Campaign performance data - use live data from API
  const campaignsData = topCampaigns.length > 0 ? topCampaigns : [];

  // Recent captures data - use live data from API
  const capturesData = recentCaptures.length > 0 ? recentCaptures.slice(0, 5) : [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Advanced Analytics Dashboard</h1>
        <p className="text-slate-400">Comprehensive tracking and performance metrics</p>
      </div>

      {/* Controls - Mobile Optimized */}
      <div className="space-y-4 mb-8">
        {/* Top Row - Filter and Search */}
        <div className="flex flex-col sm:flex-row gap-4">
          <Select defaultValue="all">
            <SelectTrigger className="w-full sm:w-[180px] bg-slate-800 border-slate-700 text-white">
              <SelectValue placeholder="All" />
            </SelectTrigger>
            <SelectContent className="bg-slate-800 border-slate-700">
              <SelectItem value="all">All</SelectItem>
              <SelectItem value="campaigns">Campaigns</SelectItem>
              <SelectItem value="links">Links</SelectItem>
            </SelectContent>
          </Select>
          
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
              <input
                type="text"
                placeholder="Search campaigns, emails, tracking..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-md text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>
        
        {/* Bottom Row - Time Period and Action Buttons */}
        <div className="flex flex-wrap gap-2 justify-center sm:justify-start">
          <Button
            variant={period === '24h' ? 'default' : 'outline'}
            size="sm"
            onClick={() => handlePeriodChange('24h')}
            className={period === '24h' ? 'bg-blue-600 hover:bg-blue-700' : 'border-slate-600 text-slate-300 hover:bg-slate-700'}
          >
            24h
          </Button>
          <Button
            variant={period === '7d' ? 'default' : 'outline'}
            size="sm"
            onClick={() => handlePeriodChange('7d')}
            className={period === '7d' ? 'bg-blue-600 hover:bg-blue-700' : 'border-slate-600 text-slate-300 hover:bg-slate-700'}
          >
            7d
          </Button>
          <Button
            variant={period === '30d' ? 'default' : 'outline'}
            size="sm"
            onClick={() => handlePeriodChange('30d')}
            className={period === '30d' ? 'bg-blue-600 hover:bg-blue-700' : 'border-slate-600 text-slate-300 hover:bg-slate-700'}
          >
            30d
          </Button>
          <Button
            variant={period === '90d' ? 'default' : 'outline'}
            size="sm"
            onClick={() => handlePeriodChange('90d')}
            className={period === '90d' ? 'bg-blue-600 hover:bg-blue-700' : 'border-slate-600 text-slate-300 hover:bg-slate-700'}
          >
            90d
          </Button>
          <Button
            onClick={handleRefresh}
            size="sm"
            variant="outline"
            className="border-slate-600 text-slate-300 hover:bg-slate-700"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button 
            size="sm" 
            variant="outline" 
            className="h-9 px-3"
            onClick={handleExport}
          >
            <Download className="h-4 w-4 mr-1" />
            Export
          </Button>
        </div>
      </div>

      {/* Compact Metric Cards Grid - Perfect 8-Grid Layout */}
      {/* Compact Metric Cards Grid - 7-Grid Layout */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-3 mb-8">
        {/* Total Links */}
        <Card className="hover:shadow-md transition-all cursor-pointer bg-slate-800/50 border-slate-700/50">
          <CardContent className="p-3">
            <div className="flex flex-col gap-1">
              <div className="flex items-center justify-between">
                <p className="text-xs font-medium text-slate-400">Total Links</p>
                <Link className="h-4 w-4 text-blue-500/80" />
              </div>
              <p className="text-xl font-bold text-white">{stats.totalLinks || 6}</p>
            </div>
          </CardContent>
        </Card>

        {/* Total Clicks */}
        <Card className="hover:shadow-md transition-all cursor-pointer bg-slate-800/50 border-slate-700/50">
          <CardContent className="p-3">
            <div className="flex flex-col gap-1">
              <div className="flex items-center justify-between">
                <p className="text-xs font-medium text-slate-400">Total Clicks</p>
                <MousePointer className="h-4 w-4 text-green-500/80" />
              </div>
              <p className="text-xl font-bold text-white">{stats.totalClicks || 4}</p>
            </div>
          </CardContent>
        </Card>

        {/* Real Visitors */}
        <Card className="hover:shadow-md transition-all cursor-pointer bg-slate-800/50 border-slate-700/50">
          <CardContent className="p-3">
            <div className="flex flex-col gap-1">
              <div className="flex items-center justify-between">
                <p className="text-xs font-medium text-slate-400">Real Visitors</p>
                <Eye className="h-4 w-4 text-purple-500/80" />
              </div>
              <p className="text-xl font-bold text-white">{additionalStats.realVisitors}</p>
            </div>
          </CardContent>
        </Card>

        {/* Captured Emails */}
        <Card className="hover:shadow-md transition-all cursor-pointer bg-slate-800/50 border-slate-700/50">
          <CardContent className="p-3">
            <div className="flex flex-col gap-1">
              <div className="flex items-center justify-between">
                <p className="text-xs font-medium text-slate-400">Captured Emails</p>
                <Mail className="h-4 w-4 text-orange-500/80" />
              </div>
              <p className="text-xl font-bold text-white">{additionalStats.capturedEmails}</p>
            </div>
          </CardContent>
        </Card>

        {/* Active Links */}
        <Card className="hover:shadow-md transition-all cursor-pointer bg-slate-800/50 border-slate-700/50">
          <CardContent className="p-3">
            <div className="flex flex-col gap-1">
              <div className="flex items-center justify-between">
                <p className="text-xs font-medium text-slate-400">Active Links</p>
                <TrendingUp className="h-4 w-4 text-emerald-500/80" />
              </div>
              <p className="text-xl font-bold text-white">{additionalStats.activeLinks}</p>
            </div>
          </CardContent>
        </Card>

        {/* Conversion Rate */}
        <Card className="hover:shadow-md transition-all cursor-pointer bg-slate-800/50 border-slate-700/50">
          <CardContent className="p-3">
            <div className="flex flex-col gap-1">
              <div className="flex items-center justify-between">
                <p className="text-xs font-medium text-slate-400">Conversion Rate</p>
                <BarChartIcon className="h-4 w-4 text-yellow-500/80" />
              </div>
              <p className="text-xl font-bold text-white">{additionalStats.conversionRate}%</p>
            </div>
          </CardContent>
        </Card>

        {/* Countries */}
        <Card className="hover:shadow-md transition-all cursor-pointer bg-slate-800/50 border-slate-700/50">
          <CardContent className="p-3">
            <div className="flex flex-col gap-1">
              <div className="flex items-center justify-between">
                <p className="text-xs font-medium text-slate-400">Countries</p>
                <Globe className="h-4 w-4 text-cyan-500/80" />
              </div>
              <p className="text-xl font-bold text-white">{additionalStats.countries}</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Grid - Side by Side */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Performance Over Time Chart */}
        <Card className="hover:shadow-md transition-shadow">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg font-semibold">Performance Over Time</CardTitle>
            <p className="text-xs text-muted-foreground">Clicks, visitors, and email captures</p>
          </CardHeader>
          <CardContent className="p-4 pt-0">
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={performanceData}>
                <defs>
                  <linearGradient id="colorClicks" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0.1}/>
                  </linearGradient>
                  <linearGradient id="colorVisitors" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.1}/>
                  </linearGradient>
                  <linearGradient id="colorEmails" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0.1}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" className="opacity-20" />
                <XAxis 
                  dataKey="date" 
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis 
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'hsl(var(--background))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px',
                    fontSize: '12px'
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="clicks"
                  stroke="#8b5cf6"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorClicks)"
                  name="Clicks"
                />
                <Area
                  type="monotone"
                  dataKey="visitors"
                  stroke="#06b6d4"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorVisitors)"
                  name="Visitors"
                />
                <Area
                  type="monotone"
                  dataKey="emails"
                  stroke="#10b981"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorEmails)"
                  name="Email Captures"
                />
              </AreaChart>
            </ResponsiveContainer>
            <div className="flex justify-center gap-4 mt-3">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-purple-500"></div>
                <span className="text-xs text-muted-foreground">Clicks</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-cyan-500"></div>
                <span className="text-xs text-muted-foreground">Visitors</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <span className="text-xs text-muted-foreground">Email Captures</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Device Breakdown Chart */}
        <Card className="hover:shadow-md transition-shadow">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg font-semibold">Device Breakdown</CardTitle>
            <p className="text-xs text-muted-foreground">Traffic distribution by device type</p>
          </CardHeader>
          <CardContent className="p-4 pt-0">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={deviceData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={110}
                  paddingAngle={3}
                  dataKey="value"
                >
                  {deviceData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value, name) => [value.toLocaleString(), name]}
                  contentStyle={{
                    backgroundColor: 'hsl(var(--background))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px',
                    fontSize: '12px'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="flex justify-center gap-4 mt-3">
              {deviceData.map((item, index) => (
                <div key={index} className="flex items-center gap-2">
                  <div 
                    className="w-3 h-3 rounded-full" 
                    style={{ backgroundColor: item.color }}
                  ></div>
                  <span className="text-xs text-muted-foreground">
                    {item.name}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Bottom Three Large Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Top Countries Card */}
        <Card className="hover:shadow-md transition-shadow">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg font-semibold">Top Countries</CardTitle>
            <p className="text-xs text-muted-foreground">Geographic distribution</p>
          </CardHeader>
          <CardContent className="p-4 pt-0">
            <div className="space-y-3">
              {countriesData.map((country, index) => (
                <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-muted/50 hover:bg-muted transition-colors">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{country.flag}</span>
                    <div>
                      <p className="text-sm font-medium">{country.country}</p>
                      <p className="text-xs text-muted-foreground">
                        {country.clicks} clicks • {country.emails} emails
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold">{country.percentage}%</p>
                    <div className="w-16 h-1.5 bg-muted rounded-full mt-1 overflow-hidden">
                      <div 
                        className="h-full bg-blue-500 rounded-full transition-all"
                        style={{ width: `${country.percentage}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Campaign Performance Card */}
        <Card className="hover:shadow-md transition-shadow">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg font-semibold">Campaign Performance</CardTitle>
            <p className="text-xs text-muted-foreground">Top performing campaigns</p>
          </CardHeader>
          <CardContent className="p-4 pt-0">
            <div className="space-y-3">
              {campaignsData.map((campaign, index) => (
                <div key={index} className="p-3 rounded-lg bg-muted/50 hover:bg-muted transition-colors">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <p className="text-sm font-medium">{campaign.name}</p>
                      <p className="text-xs text-muted-foreground">ID: {campaign.id}</p>
                    </div>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      campaign.status === 'active' 
                        ? 'bg-green-500/20 text-green-600 dark:text-green-400' 
                        : 'bg-gray-500/20 text-gray-600 dark:text-gray-400'
                    }`}>
                      {campaign.status}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-xs text-muted-foreground">
                    <span>{campaign.clicks} clicks</span>
                    <span>{campaign.emails} emails</span>
                    <span className="font-medium">{campaign.conversion} conversion</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Recent Captures Card */}
        <Card className="hover:shadow-md transition-shadow">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg font-semibold">Recent Captures</CardTitle>
            <p className="text-xs text-muted-foreground">Latest email captures</p>
          </CardHeader>
          <CardContent className="p-4 pt-0">
            {capturesData.length > 0 ? (
              <div className="space-y-3">
                {capturesData.map((capture, index) => (
                  <div key={index} className="p-3 rounded-lg bg-muted/50 hover:bg-muted transition-colors">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
                        <Mail className="h-4 w-4 text-primary" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium truncate">{capture.email}</p>
                        <p className="text-xs text-muted-foreground">{capture.timestamp}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-8 text-center">
                <Mail className="h-12 w-12 text-muted-foreground/50 mb-3" />
                <p className="text-sm text-muted-foreground">No email captures yet</p>
                <p className="text-xs text-muted-foreground mt-1">Captured emails will appear here</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
