import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Label } from './ui/label'
import { Textarea } from './ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select'
import { Badge } from './ui/badge'
import { Progress } from './ui/progress'
import { 
  Plus,
  Edit,
  Trash2,
  Play,
  Pause,
  TrendingUp,
  Target,
  Users,
  MousePointer,
  Mail,
  RefreshCw,
  Download
} from 'lucide-react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from './ui/dialog'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts'

const Campaign = () => {
  const [campaigns, setCampaigns] = useState([])
  const [loading, setLoading] = useState(true)
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [newCampaign, setNewCampaign] = useState({
    name: '',
    description: '',
    targetUrl: '',
    status: 'active'
  })

  useEffect(() => {
    fetchCampaigns()
  }, [])

  const fetchCampaigns = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/campaigns', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        setCampaigns(data.campaigns || [])
      }
    } catch (error) {
      console.error('Error fetching campaigns:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateCampaign = async () => {
    try {
      const response = await fetch('/api/campaigns', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(newCampaign)
      })

      if (response.ok) {
        setIsCreateModalOpen(false)
        setNewCampaign({
          name: '',
          description: '',
          targetUrl: '',
          status: 'active'
        })
        fetchCampaigns()
      }
    } catch (error) {
      console.error('Error creating campaign:', error)
    }
  }

  const toggleCampaignStatus = async (campaignId, currentStatus) => {
    try {
      const newStatus = currentStatus === 'active' ? 'paused' : 'active'
      const response = await fetch(`/api/campaigns/${campaignId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ status: newStatus })
      })

      if (response.ok) {
        fetchCampaigns()
      }
    } catch (error) {
      console.error('Error updating campaign:', error)
    }
  }

  const deleteCampaign = async (campaignId) => {
    if (!confirm('Are you sure you want to delete this campaign?')) return

    try {
      const response = await fetch(`/api/campaigns/${campaignId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })

      if (response.ok) {
        fetchCampaigns()
      }
    } catch (error) {
      console.error('Error deleting campaign:', error)
    }
  }

  const handleRefresh = () => {
    fetchCampaigns()
  }

  const handleExport = () => {
    const csvData = [
      ['Campaign', 'Status', 'Clicks', 'Conversions', 'Rate'],
      ...campaigns.map(c => [c.name, c.status, c.clicks, c.conversions, `${c.conversion_rate}%`])
    ]
    
    const csvContent = csvData.map(row => row.join(',')).join('\n')
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `campaigns-${new Date().toISOString().split('T')[0]}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Campaign Management</h1>
          <p className="text-slate-400">Create and manage your marketing campaigns</p>

        <Dialog open={isCreateModalOpen} onOpenChange={setIsCreateModalOpen}>
          <DialogTrigger asChild>
            <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
              <Plus className="h-4 w-4 mr-2" />
              Create Campaign
            </Button>
          </DialogTrigger>
          <DialogContent className="bg-slate-800 border-slate-700">
            <DialogHeader>
              <DialogTitle className="text-white">Create New Campaign</DialogTitle>
              <DialogDescription className="text-slate-400">
                Set up a new tracking campaign
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label htmlFor="name" className="text-white">Campaign Name</Label>
                <Input
                  id="name"
                  value={newCampaign.name}
                  onChange={(e) => setNewCampaign({ ...newCampaign, name: e.target.value })}
                  className="bg-slate-700 border-slate-600 text-white"
                  placeholder="Enter campaign name"
                />

              <div className="space-y-2">
                <Label htmlFor="description" className="text-white">Description</Label>
                <Textarea
                  id="description"
                  value={newCampaign.description}
                  onChange={(e) => setNewCampaign({ ...newCampaign, description: e.target.value })}
                  className="bg-slate-700 border-slate-600 text-white"
                  placeholder="Describe your campaign"
                  rows={3}
                />

              <div className="space-y-2">
                <Label htmlFor="targetUrl" className="text-white">Target URL</Label>
                <Input
                  id="targetUrl"
                  type="url"
                  value={newCampaign.targetUrl}
                  onChange={(e) => setNewCampaign({ ...newCampaign, targetUrl: e.target.value })}
                  className="bg-slate-700 border-slate-600 text-white"
                  placeholder="https://example.com"
                />


            <DialogFooter>
              <Button variant="outline" onClick={() => setIsCreateModalOpen(false)} className="border-slate-600">
                Cancel
              </Button>
              <Button onClick={handleCreateCampaign} className="bg-blue-600 hover:bg-blue-700">
                Create Campaign
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>


      {/* Controls */}
      <div className="flex gap-2 mb-6">
        <Button variant="outline" size="sm" onClick={handleRefresh} className="border-slate-600 text-slate-300 hover:bg-slate-700">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
        <Button variant="outline" size="sm" onClick={handleExport} className="border-slate-600 text-slate-300 hover:bg-slate-700">
          <Download className="h-4 w-4 mr-2" />
          Export
        </Button>
      </div>

      {/* Campaign Summary Cards - Mobile: 2 cols, Desktop: 4 cols */}
      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        <Card className="hover:shadow-md transition-all cursor-pointer bg-card/50 border-border/50">
          <CardContent className="p-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1">Total Campaigns</p>
                <p className="text-xl font-bold text-foreground">{campaigns.length}</p>
              </div>
              <div className="p-2 bg-blue-500/20 rounded-full">
                <Target className="h-5 w-5 text-blue-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-all cursor-pointer bg-card/50 border-border/50">
          <CardContent className="p-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1">Active Campaigns</p>
                <p className="text-xl font-bold text-foreground">
                  {campaigns.filter(c => c.status === 'active').length}
                </p>
              </div>
              <div className="p-2 bg-green-500/20 rounded-full">
                <Play className="h-5 w-5 text-green-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-all cursor-pointer bg-card/50 border-border/50">
          <CardContent className="p-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1">Total Clicks</p>
                <p className="text-xl font-bold text-foreground">
                  {campaigns.reduce((sum, c) => sum + (c.clicks || 0), 0).toLocaleString()}
                </p>
              </div>
              <div className="p-2 bg-purple-500/20 rounded-full">
                <MousePointer className="h-5 w-5 text-purple-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-all cursor-pointer bg-card/50 border-border/50">
          <CardContent className="p-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1">Avg. Conversion</p>
                <p className="text-xl font-bold text-foreground">
                  {campaigns.length > 0 
                    ? (campaigns.reduce((sum, c) => sum + (c.conversion_rate || 0), 0) / campaigns.length).toFixed(1)
                    : 0}%
                </p>
              </div>
              <div className="p-2 bg-orange-500/20 rounded-full">
                <TrendingUp className="h-5 w-5 text-orange-400" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Campaign List */}
      <Card className="bg-card border-border">
        <CardHeader>
          <CardTitle className="text-base font-semibold text-foreground">All Campaigns</CardTitle>
          <CardDescription className="text-muted-foreground">Manage and monitor your campaigns</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
	            <Table>
	              <TableHeader>
	                <TableRow className="border-border">
	                  <TableHead className="text-muted-foreground">Name</TableHead>
	                  <TableHead className="text-muted-foreground hidden sm:table-cell">Status</TableHead>
	                  <TableHead className="text-muted-foreground hidden md:table-cell">Clicks</TableHead>
	                  <TableHead className="text-muted-foreground hidden md:table-cell">Conversion</TableHead>
	                  <TableHead className="text-muted-foreground text-right">Actions</TableHead>
	                </TableRow>
	              </TableHeader>
	              <TableBody>
            {/* Mobile responsive layout wrapper */}
{campaigns.length > 0 ? (
	              campaigns.map((campaign) => (
	                <TableRow key={campaign.id} className="border-border hover:bg-accent/50">
	                  <TableCell className="text-foreground font-medium">
	                    <div className="flex flex-col">
	                      <span>{campaign.name}</span>
	                      <span className="text-xs text-muted-foreground hidden sm:block">{campaign.description}</span>
	                    </div>
	                  </TableCell>
	                  <TableCell className="hidden sm:table-cell">
	                    <Badge variant={campaign.status === 'active' ? 'default' : 'secondary'}>
	                      {campaign.status}
	                    </Badge>
	                  </TableCell>
	                  <TableCell className="text-foreground hidden md:table-cell">
	                    {campaign.clicks || 0}
	                  </TableCell>
	                  <TableCell className="text-foreground hidden md:table-cell">
	                    <div className="flex items-center gap-2">
	                      <span>{campaign.conversion_rate || 0}%</span>
	                      <Progress value={campaign.conversion_rate || 0} className="h-2 w-20" />
	                    </div>
	                  </TableCell>
	                  <TableCell className="text-right flex justify-end gap-2">
	                    <Button
	                      size="sm"
	                      variant="outline"
	                      onClick={() => toggleCampaignStatus(campaign.id, campaign.status)}
	                      className="border-border text-muted-foreground hover:bg-accent hover:text-foreground"
	                      title={campaign.status === 'active' ? 'Pause Campaign' : 'Activate Campaign'}
	                    >
	                      {campaign.status === 'active' ? (
	                        <Pause className="h-4 w-4" />
	                      ) : (
	                        <Play className="h-4 w-4" />
	                      )}
	                    </Button>
	                    <Button
	                      size="sm"
	                      variant="outline"
	                      className="border-border text-muted-foreground hover:bg-accent hover:text-foreground"
	                      title="Edit Campaign"
	                    >
	                      <Edit className="h-4 w-4" />
	                    </Button>
	                    <Button
	                      size="sm"
	                      variant="outline"
	                      onClick={() => deleteCampaign(campaign.id)}
	                      className="border-red-600 text-red-400 hover:bg-red-600/10"
	                      title="Delete Campaign"
	                    >
	                      <Trash2 className="h-4 w-4" />
	                    </Button>
	                  </TableCell>
	                </TableRow>
	              ))
	            ) : (
	              <TableRow>
	                <TableCell colSpan={5}>
	                  <div className="text-center py-12">
	                    <Target className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
	                    <h3 className="text-xl font-semibold text-foreground mb-2">No campaigns yet</h3>
	                    <p className="text-muted-foreground mb-4">Create your first campaign to start tracking</p>
	                    <Button onClick={() => setIsCreateModalOpen(true)} className="bg-blue-600 hover:bg-blue-700">
	                      <Plus className="h-4 w-4 mr-2" />
	                      Create Campaign
	                    </Button>
	                  </div>
	                </TableCell>
	              </TableRow>
	            )}
	          </TableBody>
	        </Table>
	      </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Campaign
