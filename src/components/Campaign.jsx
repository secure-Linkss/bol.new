import React, { useState, useEffect } from 'react'
import { toast } from 'sonner'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { Progress } from './ui/progress'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog'
import { Input } from './ui/input'
import { Label } from './ui/label'
import { Textarea } from './ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart,
  Line
} from 'recharts'
import { 
  Plus, 
  Target, 
  TrendingUp, 
  Users, 
  MousePointer, 
  Mail,
  ChevronDown,
  ChevronUp,
  Edit,
  Trash2,
  Play,
  Pause,
  BarChart3,
  Calendar,
  Globe
} from 'lucide-react'

const Campaign = () => {
  const [campaigns, setCampaigns] = useState([])
  const [loading, setLoading] = useState(true)
  const [expandedCampaign, setExpandedCampaign] = useState(null)
  const [analytics, setAnalytics] = useState({
    totalClicks: 0,
    realVisitors: 0,
    botsBlocked: 0,
    activeCampaigns: 0
  })
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [newCampaign, setNewCampaign] = useState({
    name: '',
    description: '',
    targetUrl: '',
    previewUrl: '',
    expiration: 'never'
  })

  useEffect(() => {
    fetchCampaigns()
    fetchAnalytics()
  }, [])

  const fetchCampaigns = async () => {
    try {
      // Use the dashboard endpoint to get campaign data
      const response = await fetch('/api/analytics/dashboard?period=30')
      
      if (response.ok) {
        const data = await response.json()
        setCampaigns(data.campaigns || [])
      } else {
        console.error('Failed to fetch campaigns')
      }
    } catch (error) {
      console.error('Error fetching campaigns:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchAnalytics = async () => {
    try {
      const response = await fetch('/api/analytics/dashboard?period=30')
      
      if (response.ok) {
        const data = await response.json()
        setAnalytics({
          totalClicks: data.analytics?.totalClicks || 0,
          realVisitors: data.analytics?.realVisitors || 0,
          botsBlocked: (data.analytics?.totalClicks || 0) - (data.analytics?.realVisitors || 0),
          activeCampaigns: (data.campaigns || []).filter(c => c.status === 'active').length
        })
      }
    } catch (error) {
      console.error('Error fetching campaign analytics:', error)
    }
  }

  const toggleCampaignExpansion = (e, campaignId) => {
    e.stopPropagation();
    setExpandedCampaign(expandedCampaign === campaignId ? null : campaignId);
  };

  const handleCreateCampaign = async (e) => {
    e.preventDefault()
    
    if (!newCampaign.name.trim() || !newCampaign.targetUrl.trim()) {
      toast.error('Please fill in all required fields')
      return
    }
    
    try {
      const response = await fetch('/api/links', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          original_url: newCampaign.targetUrl.trim(),
          preview_url: newCampaign.previewUrl.trim() || null,
          campaign_name: newCampaign.name.trim(),
          title: newCampaign.name.trim(),
          description: newCampaign.description.trim() || null,
          expiration: newCampaign.expiration
        })
      })
      
      if (response.ok) {
        // Reset form and close dialog
        setNewCampaign({
          name: '',
          description: '',
          targetUrl: '',
          previewUrl: '',
          expiration: 'never'
        })
        setShowCreateDialog(false)
        
        // Refresh campaigns list
        await fetchCampaigns()
        toast.success('Campaign created successfully!')
      } else {
        const errorData = await response.json()
        toast.error(errorData.error || 'Failed to create campaign')
      }
    } catch (error) {
      console.error('Error creating campaign:', error)
      toast.error('Failed to create campaign')
    }
  }

  const handleDeleteCampaign = async (campaignId) => {
    if (!confirm('Are you sure you want to delete this campaign?')) {
      return
    }
    
    try {
      const response = await fetch(`/api/links/${campaignId}`, {
        method: 'DELETE'
      })
      
      if (response.ok) {
        await fetchCampaigns()
        toast.success('Campaign deleted successfully!')
      } else {
        toast.error('Failed to delete campaign')
      }
    } catch (error) {
      console.error('Error deleting campaign:', error)
      toast.error('Failed to delete campaign')
    }
  }

  const handleToggleCampaign = async (campaignId, currentStatus) => {
    try {
      const newStatus = currentStatus === 'active' ? 'paused' : 'active'
      const response = await fetch(`/api/links/${campaignId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          is_active: newStatus === 'active'
        })
      })
      
      if (response.ok) {
        await fetchCampaigns()
        toast.success('Campaign status updated successfully!')
      } else {
        toast.error('Failed to update campaign status')
      }
    } catch (error) {
      console.error('Error updating campaign:', error)
      toast.error('Failed to update campaign')
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'paused':
        return 'bg-yellow-100 text-yellow-800'
      case 'completed':
        return 'bg-blue-100 text-blue-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const fetchCampaignPerformance = async (campaignId) => {
    try {
      const response = await fetch(`/api/analytics/campaign/${campaignId}/performance`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        return data.performance_data || []
      } else {
        console.error(`Failed to fetch performance data for campaign ${campaignId}`)
        return []
      }
    } catch (error) {
      console.error(`Error fetching performance data for campaign ${campaignId}:`, error)
      return []
    }
  }

  const renderPerformanceChart = (campaign) => {
    const [performanceData, setPerformanceData] = useState([])

    useEffect(() => {
      if (campaign.id) {
        fetchCampaignPerformance(campaign.id).then(setPerformanceData)
      }
    }, [campaign.id])

    return (
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={performanceData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="clicks" stroke="#8884d8" strokeWidth={2} />
          <Line type="monotone" dataKey="visitors" stroke="#82ca9d" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    )
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-2">Loading campaigns...</span>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold">Campaigns</h2>
          <p className="text-muted-foreground">Manage and monitor your tracking campaigns</p>
        </div>
        <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Create Campaign
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[450px]">
              <DialogHeader>
                <DialogTitle>Create New Campaign</DialogTitle>
                <DialogDescription>
                  Set up a new tracking campaign with custom parameters and settings.
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleCreateCampaign} className="space-y-4">
                <div className="space-y-3">
                  <div className="space-y-2">
                    <Label htmlFor="campaign-name">Campaign Name *</Label>
                    <Input
                      id="campaign-name"
                      placeholder="Enter campaign name"
                      value={newCampaign.name}
                      onChange={(e) => setNewCampaign({...newCampaign, name: e.target.value})}
                      required
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="target-url">Target URL *</Label>
                    <Input
                      id="target-url"
                      type="url"
                      placeholder="https://example.com"
                      value={newCampaign.targetUrl}
                      onChange={(e) => setNewCampaign({...newCampaign, targetUrl: e.target.value})}
                      required
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="preview-url">Preview URL (Optional)</Label>
                    <Input
                      id="preview-url"
                      type="url"
                      placeholder="https://preview.example.com"
                      value={newCampaign.previewUrl}
                      onChange={(e) => setNewCampaign({...newCampaign, previewUrl: e.target.value})}
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="description">Description (Optional)</Label>
                    <Textarea
                      id="description"
                      placeholder="Describe your campaign..."
                      value={newCampaign.description}
                      onChange={(e) => setNewCampaign({...newCampaign, description: e.target.value})}
                      rows={3}
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="expiration">Link Expiration</Label>
                    <Select 
                      value={newCampaign.expiration} 
                      onValueChange={(value) => setNewCampaign({...newCampaign, expiration: value})}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select expiration" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="never">Never Expires</SelectItem>
                        <SelectItem value="5h">5 Hours</SelectItem>
                        <SelectItem value="10h">10 Hours</SelectItem>
                        <SelectItem value="24h">24 Hours</SelectItem>
                        <SelectItem value="48h">48 Hours</SelectItem>
                        <SelectItem value="72h">72 Hours</SelectItem>
                        <SelectItem value="7d">Weekly</SelectItem>
                        <SelectItem value="30d">Monthly</SelectItem>
                        <SelectItem value="365d">Yearly</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                
                <DialogFooter>
                  <Button type="button" variant="outline" onClick={() => setShowCreateDialog(false)}>
                    Cancel
                  </Button>
                  <Button type="submit">
                    <Plus className="h-4 w-4 mr-2" />
                    Create Campaign
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>
        
      {/* Analytics Overview */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Clicks</CardTitle>
            <MousePointer className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics.totalClicks}</div>
            <p className="text-xs text-muted-foreground">
              Across all campaigns
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Real Visitors</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics.realVisitors}</div>
            <p className="text-xs text-muted-foreground">
              Unique human visitors
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Bots Blocked</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics.botsBlocked}</div>
            <p className="text-xs text-muted-foreground">
              Automated traffic filtered
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Campaigns</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics.activeCampaigns}</div>
            <p className="text-xs text-muted-foreground">
              Currently running
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Campaigns List */}
      <Card>
        <CardHeader>
          <CardTitle>Campaign Performance</CardTitle>
          <CardDescription>
            Overview of all your tracking campaigns
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {campaigns.map((campaign) => (
              <div key={campaign.id} className="border rounded-lg p-4 space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                      <Target className="h-5 w-5 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold">{campaign.name}</h3>
                      <p className="text-sm text-muted-foreground">ID: {campaign.trackingId}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <Badge className={getStatusColor(campaign.status)}>
                      {campaign.status}
                    </Badge>
                    
                    <div className="flex items-center space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleToggleCampaign(campaign.id, campaign.status)}
                      >
                        {campaign.status === 'active' ? (
                          <Pause className="h-4 w-4" />
                        ) : (
                          <Play className="h-4 w-4" />
                        )}
                      </Button>
                      
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={(e) => toggleCampaignExpansion(e, campaign.id)}
                      >
                        {expandedCampaign === campaign.id ? (
                          <ChevronUp className="h-4 w-4" />
                        ) : (
                          <ChevronDown className="h-4 w-4" />
                        )}
                      </Button>
                      
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleDeleteCampaign(campaign.id)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
                
                {/* Campaign Metrics */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <p className="text-2xl font-bold">{campaign.clicks}</p>
                    <p className="text-sm text-muted-foreground">Clicks</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold">{campaign.visitors}</p>
                    <p className="text-sm text-muted-foreground">Visitors</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold">{campaign.emails}</p>
                    <p className="text-sm text-muted-foreground">Emails</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold">{campaign.conversionRate}%</p>
                    <p className="text-sm text-muted-foreground">Conversion</p>
                  </div>
                </div>
                
                {/* Expanded Details */}
                {expandedCampaign === campaign.id && (
                  <div className="border-t pt-4 space-y-4">
                    <div className="grid gap-4 md:grid-cols-2">
                      {/* Performance Chart */}
                      <div>
                        <h4 className="font-medium mb-2">7-Day Performance</h4>
                        {renderPerformanceChart(campaign)}
                      </div>
                      
                      {/* Campaign Details */}
                      <div className="space-y-4">
                        <div>
                          <h4 className="font-medium mb-2">Campaign Details</h4>
                          <div className="space-y-2 text-sm">
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Created:</span>
                              <span>{campaign.created ? new Date(campaign.created).toLocaleDateString() : 'N/A'}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Status:</span>
                              <Badge className={getStatusColor(campaign.status)}>
                                {campaign.status}
                              </Badge>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Tracking ID:</span>
                              <span className="font-mono">{campaign.trackingId}</span>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <h4 className="font-medium mb-2">Performance Metrics</h4>
                          <div className="space-y-2">
                            <div className="flex justify-between items-center">
                              <span className="text-sm text-muted-foreground">Click-through Rate</span>
                              <span className="text-sm font-medium">{campaign.conversionRate}%</span>
                            </div>
                            <Progress value={campaign.conversionRate} className="h-2" />
                            
                            <div className="flex justify-between items-center">
                              <span className="text-sm text-muted-foreground">Visitor Engagement</span>
                              <span className="text-sm font-medium">
                                {campaign.visitors > 0 ? Math.round((campaign.emails / campaign.visitors) * 100) : 0}%
                              </span>
                            </div>
                            <Progress 
                              value={campaign.visitors > 0 ? (campaign.emails / campaign.visitors) * 100 : 0} 
                              className="h-2" 
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
            
            {campaigns.length === 0 && (
              <div className="text-center py-8">
                <Target className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-2">No campaigns yet</h3>
                <p className="text-muted-foreground mb-4">
                  Create your first campaign to start tracking links
                </p>
                <Button onClick={() => setShowCreateDialog(true)}>
                  <Plus className="h-4 w-4 mr-2" />
                  Create Your First Campaign
                </Button>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Campaign

