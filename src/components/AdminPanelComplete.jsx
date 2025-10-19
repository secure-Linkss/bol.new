import { useState, useEffect } from 'react';
import { toast } from 'sonner';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
  Users, FolderKanban, Shield, CreditCard, MessageSquare, FileText, Settings, LayoutDashboard,
  UserCheck, UserX, Trash2, Edit, Eye, MoreVertical, Download, RefreshCw, AlertTriangle,
  Search, Filter, Plus, ChevronDown, ChevronUp, TrendingUp, TrendingDown, Activity, Check, X, Clock,
  Globe, Copy, Zap
} from 'lucide-react';
import {
  DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger,
  DropdownMenuSeparator, DropdownMenuLabel,
} from '@/components/ui/dropdown-menu';
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from '@/components/ui/select';
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from '@/components/ui/table';
import {
  Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle,
} from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Alert, AlertDescription } from '@/components/ui/alert';

const AdminPanelComplete = () => {
  const [activeTab, setActiveTab] = useState('dashboard')

  // Helper function to make API calls
  const apiCall = async (endpoint, options = {}) => {
    const token = localStorage.getItem('token')
    const response = await fetch(endpoint, {
      ...options,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Request failed')
    }
    
    return response.json()
  }

  return (
    <div className="min-h-screen bg-gray-950 p-4 md:p-6 lg:p-8">
      <div className="max-w-[1600px] mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-white mb-2">Admin Panel</h1>
          <p className="text-gray-400">Enterprise-grade system administration and monitoring</p>
        </div>

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="w-full justify-start overflow-x-auto bg-gray-900 border-gray-800 border-b rounded-none">
            <TabsTrigger value="dashboard" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
              <LayoutDashboard className="w-4 h-4 mr-2" />
              Dashboard
            </TabsTrigger>
            <TabsTrigger value="users" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
              <Users className="w-4 h-4 mr-2" />
              Users
            </TabsTrigger>
            <TabsTrigger value="campaigns" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
              <FolderKanban className="w-4 h-4 mr-2" />
              Campaigns
            </TabsTrigger>
            <TabsTrigger value="security" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
              <Shield className="w-4 h-4 mr-2" />
              Security
            </TabsTrigger>
            <TabsTrigger value="subscriptions" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
              <CreditCard className="w-4 h-4 mr-2" />
              Subscriptions
            </TabsTrigger>
            <TabsTrigger value="tickets" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
              <MessageSquare className="w-4 h-4 mr-2" />
              Support
            </TabsTrigger>
            <TabsTrigger value="audit" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
              <FileText className="w-4 h-4 mr-2" />
              Audit Logs
            </TabsTrigger>
            <TabsTrigger value="settings" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
              <Settings className="w-4 h-4 mr-2" />
              Settings
            </TabsTrigger>
          </TabsList>

          {/* Dashboard Tab */}
          <TabsContent value="dashboard" className="mt-6">
            <DashboardTab apiCall={apiCall} />
          </TabsContent>

          {/* User Management Tab */}
          <TabsContent value="users" className="mt-6">
            <UserManagementTab apiCall={apiCall} />
          </TabsContent>

          {/* Campaign Management Tab */}
          <TabsContent value="campaigns" className="mt-6">
            <CampaignManagementTab apiCall={apiCall} />
          </TabsContent>

          {/* Security Tab */}
          <TabsContent value="security" className="mt-6">
            <SecurityTab apiCall={apiCall} />
          </TabsContent>

          {/* Subscriptions Tab */}
          <TabsContent value="subscriptions" className="mt-6">
            <SubscriptionsTab apiCall={apiCall} />
          </TabsContent>

          {/* Support Tickets Tab */}
          <TabsContent value="tickets" className="mt-6">
            <TicketsTab apiCall={apiCall} />
          </TabsContent>

          {/* Audit Logs Tab */}
          <TabsContent value="audit" className="mt-6">
            <AuditLogsTab apiCall={apiCall} />
          </TabsContent>

          {/* Settings Tab */}
          <TabsContent value="settings" className="mt-6">
            <SettingsTab apiCall={apiCall} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

// ============================================================================
// DASHBOARD TAB COMPONENT
// ============================================================================
const DashboardTab = ({ apiCall }) => {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      setLoading(true)
      const data = await apiCall('/api/admin/dashboard/stats')
      setStats(data)
    } catch (error) {
      toast.error('Failed to load dashboard stats')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12 text-gray-400">Loading dashboard...</div>
  }

  if (!stats) {
    return <div className="text-center py-12 text-gray-400">No data available</div>
  }

  const MetricCard = ({ title, value, icon: Icon, trend, color }) => (
    <Card className="bg-gray-900 border-gray-800 hover:border-gray-700 transition-colors">
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-400 mb-1">{title}</p>
            <p className="text-3xl font-bold text-white">{value}</p>
            {trend && (
              <p className={`text-sm mt-2 ${trend > 0 ? 'text-green-500' : 'text-red-500'}`}>
                {trend > 0 ? <TrendingUp className="w-4 h-4 inline mr-1" /> : <TrendingDown className="w-4 h-4 inline mr-1" />}
                {Math.abs(trend)}% from last month
              </p>
            )}
          </div>
          <div className={`p-4 rounded-lg ${color}`}>
            <Icon className="w-6 h-6 text-white" />
          </div>
        </div>
      </CardContent>
    </Card>
  )

  return (
    <div className="space-y-6">
      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Total Users"
          value={stats.users?.total || 0}
          icon={Users}
          color="bg-blue-600"
        />
        <MetricCard
          title="Active Campaigns"
          value={stats.campaigns?.active || 0}
          icon={FolderKanban}
          color="bg-green-600"
        />
        <MetricCard
          title="Total Links"
          value={stats.links?.total || 0}
          icon={Activity}
          color="bg-purple-600"
        />
        <MetricCard
          title="Total Clicks"
          value={stats.clicks?.total || 0}
          icon={TrendingUp}
          color="bg-orange-600"
        />
      </div>

      {/* Status Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card className="bg-gray-900 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white">User Status</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Active</span>
                <Badge className="bg-green-600">{stats.users?.active || 0}</Badge>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Pending</span>
                <Badge className="bg-yellow-600">{stats.users?.pending || 0}</Badge>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Suspended</span>
                <Badge className="bg-red-600">{stats.users?.suspended || 0}</Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-900 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white">Subscription Status</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Active Subscriptions</span>
                <Badge className="bg-green-600">{stats.subscriptions?.active || 0}</Badge>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Expired</span>
                <Badge className="bg-red-600">{stats.subscriptions?.expired || 0}</Badge>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Pending Verification</span>
                <Badge className="bg-yellow-600">{stats.subscriptions?.pending || 0}</Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card className="bg-gray-900 border-gray-800">
        <CardHeader>
          <CardTitle className="text-white">Recent Activity</CardTitle>
          <CardDescription>Latest users and campaigns</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div>
              <h3 className="text-sm font-semibold text-gray-400 mb-3">Recent Users</h3>
              <div className="space-y-2">
                {stats.recent_activity?.users?.slice(0, 5).map(user => (
                  <div key={user.id} className="flex items-center justify-between p-2 bg-gray-800 rounded">
                    <div>
                      <p className="text-white text-sm">{user.username}</p>
                      <p className="text-xs text-gray-400">{user.email}</p>
                    </div>
                    <Badge className={user.status === 'active' ? 'bg-green-600' : 'bg-yellow-600'}>
                      {user.status}
                    </Badge>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-400 mb-3">Recent Campaigns</h3>
              <div className="space-y-2">
                {stats.recent_activity?.campaigns?.slice(0, 5).map(campaign => (
                  <div key={campaign.id} className="flex items-center justify-between p-2 bg-gray-800 rounded">
                    <div>
                      <p className="text-white text-sm">{campaign.name}</p>
                      <p className="text-xs text-gray-400">{campaign.owner}</p>
                    </div>
                    <Badge className="bg-blue-600">{campaign.links} links</Badge>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// ============================================================================
// USER MANAGEMENT TAB COMPONENT
// ============================================================================
const UserManagementTab = ({ apiCall }) => {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [roleFilter, setRoleFilter] = useState('all')
  const [statusFilter, setStatusFilter] = useState('all')
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [selectedUser, setSelectedUser] = useState(null)
  const [formData, setFormData] = useState({ username: '', email: '', role: 'member', password: '' })

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      setLoading(true)
      const data = await apiCall('/api/admin/users')
      setUsers(data)
    } catch (error) {
      toast.error('Failed to load users')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateUser = async () => {
    if (!formData.username || !formData.email || !formData.password) {
      toast.error('Please fill in all required fields')
      return
    }

    try {
      await apiCall('/api/admin/users', {
        method: 'POST',
        body: JSON.stringify(formData)
      })
      toast.success('User created successfully')
      setShowCreateDialog(false)
      setFormData({ username: '', email: '', role: 'member', password: '' })
      fetchUsers()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleApprove = async (userId) => {
    try {
      await apiCall(`/api/admin/users/${userId}/approve`, { method: 'POST' })
      toast.success('User approved successfully')
      fetchUsers()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleSuspend = async (userId) => {
    try {
      await apiCall(`/api/admin/users/${userId}/suspend`, { method: 'POST' })
      toast.success('User status updated')
      fetchUsers()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleDelete = async () => {
    if (!selectedUser) return
    
    try {
      await apiCall(`/api/admin/users/${selectedUser.id}`, { method: 'DELETE' })
      toast.success('User deleted successfully')
      setShowDeleteDialog(false)
      setSelectedUser(null)
      fetchUsers()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesRole = roleFilter === 'all' || user.role === roleFilter
    const matchesStatus = statusFilter === 'all' || user.status === statusFilter
    return matchesSearch && matchesRole && matchesStatus
  })

  return (
    <div className="space-y-4">
      {/* Header Actions */}
      <div className="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
        <div className="flex-1 max-w-md">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <Input
              placeholder="Search users by username or email..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 bg-gray-900 border-gray-800 text-white placeholder-gray-500"
            />
          </div>
        </div>
        
        <div className="flex gap-2">
          <Select value={roleFilter} onValueChange={setRoleFilter}>
            <SelectTrigger className="w-[140px] bg-gray-900 border-gray-800 text-white">
              <SelectValue placeholder="Role" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Roles</SelectItem>
              <SelectItem value="member">Member</SelectItem>
              <SelectItem value="admin">Admin</SelectItem>
              <SelectItem value="main_admin">Main Admin</SelectItem>
            </SelectContent>
          </Select>

          <Select value={statusFilter} onValueChange={setStatusFilter}>
            <SelectTrigger className="w-[140px] bg-gray-900 border-gray-800 text-white">
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              <SelectItem value="active">Active</SelectItem>
              <SelectItem value="pending">Pending</SelectItem>
              <SelectItem value="suspended">Suspended</SelectItem>
            </SelectContent>
          </Select>

          <Button
            onClick={() => setShowCreateDialog(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white"
          >
            <Plus className="w-4 h-4 mr-2" />
            Create User
          </Button>
        </div>
      </div>

      {/* Users Table */}
      <Card className="bg-gray-900 border-gray-800">
        <CardContent className="p-0">
          {loading ? (
            <div className="text-center py-12 text-gray-400">Loading users...</div>
          ) : filteredUsers.length === 0 ? (
            <div className="text-center py-12 text-gray-400">No users found</div>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="border-gray-800 bg-gray-800/50">
                    <TableHead className="text-gray-400">ID</TableHead>
                    <TableHead className="text-gray-400">Username</TableHead>
                    <TableHead className="text-gray-400">Email</TableHead>
                    <TableHead className="text-gray-400">Role</TableHead>
                    <TableHead className="text-gray-400">Status</TableHead>
                    <TableHead className="text-gray-400">Plan</TableHead>
                    <TableHead className="text-gray-400">Created</TableHead>
                    <TableHead className="text-gray-400">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredUsers.map(user => (
                    <TableRow key={user.id} className="border-gray-800 hover:bg-gray-800/50 transition-colors">
                      <TableCell className="text-white">{user.id}</TableCell>
                      <TableCell className="text-white font-medium">{user.username}</TableCell>
                      <TableCell className="text-gray-400">{user.email}</TableCell>
                      <TableCell>
                        <Badge className={
                          user.role === 'main_admin' ? 'bg-purple-600' :
                          user.role === 'admin' ? 'bg-blue-600' : 'bg-gray-600'
                        }>
                          {user.role}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Badge className={
                          user.status === 'active' ? 'bg-green-600' :
                          user.status === 'pending' ? 'bg-yellow-600' : 'bg-red-600'
                        }>
                          {user.status}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-gray-400">{user.plan_type || 'N/A'}</TableCell>
                      <TableCell className="text-gray-400">
                        {user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm" className="hover:bg-gray-800">
                              <MoreVertical className="w-4 h-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end" className="bg-gray-800 border-gray-700">
                            <DropdownMenuLabel className="text-gray-300">Actions</DropdownMenuLabel>
                            <DropdownMenuSeparator className="bg-gray-700" />
                            {user.status === 'pending' && (
                              <DropdownMenuItem onClick={() => handleApprove(user.id)} className="text-green-400 cursor-pointer">
                                <UserCheck className="w-4 h-4 mr-2" />
                                Approve
                              </DropdownMenuItem>
                            )}
                            <DropdownMenuItem onClick={() => handleSuspend(user.id)} className="text-yellow-400 cursor-pointer">
                              <UserX className="w-4 h-4 mr-2" />
                              {user.status === 'suspended' ? 'Unsuspend' : 'Suspend'}
                            </DropdownMenuItem>
                            <DropdownMenuItem onClick={() => { setSelectedUser(user); setShowDeleteDialog(true); }} className="text-red-400 cursor-pointer">
                              <Trash2 className="w-4 h-4 mr-2" />
                              Delete
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Create User Dialog */}
      <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
        <DialogContent className="bg-gray-900 border-gray-800 text-white">
          <DialogHeader>
            <DialogTitle>Create New User</DialogTitle>
            <DialogDescription className="text-gray-400">
              Add a new user to the system
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label className="text-gray-300">Username</Label>
              <Input
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                placeholder="Enter username"
                className="bg-gray-800 border-gray-700 text-white mt-1"
              />
            </div>
            <div>
              <Label className="text-gray-300">Email</Label>
              <Input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                placeholder="Enter email"
                className="bg-gray-800 border-gray-700 text-white mt-1"
              />
            </div>
            <div>
              <Label className="text-gray-300">Password</Label>
              <Input
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                placeholder="Enter password"
                className="bg-gray-800 border-gray-700 text-white mt-1"
              />
            </div>
            <div>
              <Label className="text-gray-300">Role</Label>
              <Select value={formData.role} onValueChange={(val) => setFormData({...formData, role: val})}>
                <SelectTrigger className="bg-gray-800 border-gray-700 text-white mt-1">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="member">Member</SelectItem>
                  <SelectItem value="admin">Admin</SelectItem>
                  <SelectItem value="main_admin">Main Admin</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowCreateDialog(false)} className="border-gray-700">
              Cancel
            </Button>
            <Button className="bg-blue-600 hover:bg-blue-700" onClick={handleCreateUser}>
              Create User
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <DialogContent className="bg-gray-900 border-gray-800 text-white">
          <DialogHeader>
            <DialogTitle>Confirm Deletion</DialogTitle>
            <DialogDescription className="text-gray-400">
              Are you sure you want to delete user "{selectedUser?.username}"? This action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowDeleteDialog(false)} className="border-gray-700">
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleDelete} className="bg-red-600 hover:bg-red-700">
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

// ============================================================================
// CAMPAIGN MANAGEMENT TAB COMPONENT
// ============================================================================
const CampaignManagementTab = ({ apiCall }) => {
  const [campaigns, setCampaigns] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [expandedId, setExpandedId] = useState(null)
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [selectedCampaign, setSelectedCampaign] = useState(null)

  useEffect(() => {
    fetchCampaigns()
  }, [])

  const fetchCampaigns = async () => {
    try {
      setLoading(true)
      const data = await apiCall('/api/admin/campaigns/all')
      setCampaigns(Array.isArray(data) ? data : data.items || [])
    } catch (error) {
      toast.error('Failed to load campaigns')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleSuspend = async (campaignId) => {
    try {
      await apiCall(`/api/admin/campaigns/${campaignId}/suspend`, { method: 'POST' })
      toast.success('Campaign status updated')
      fetchCampaigns()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleDelete = async () => {
    if (!selectedCampaign) return
    
    try {
      await apiCall(`/api/admin/campaigns/${selectedCampaign.id}/delete`, { method: 'DELETE' })
      toast.success('Campaign deleted successfully')
      setShowDeleteDialog(false)
      setSelectedCampaign(null)
      fetchCampaigns()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleExport = async (campaignId) => {
    try {
      const data = await apiCall(`/api/admin/campaigns/${campaignId}/export`)
      const csv = data.csv || data
      const blob = new Blob([csv], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `campaign-${campaignId}.csv`
      a.click()
      toast.success('Campaign exported successfully')
    } catch (error) {
      toast.error(error.message)
    }
  }

  const filteredCampaigns = campaigns.filter(campaign => {
    const matchesSearch = campaign.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         campaign.owner?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === 'all' || campaign.status === statusFilter
    return matchesSearch && matchesStatus
  })

  return (
    <div className="space-y-4">
      {/* Header Actions */}
      <div className="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
        <div className="flex-1 max-w-md">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <Input
              placeholder="Search campaigns..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 bg-gray-900 border-gray-800 text-white placeholder-gray-500"
            />
          </div>
        </div>
        
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-[140px] bg-gray-900 border-gray-800 text-white">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="active">Active</SelectItem>
            <SelectItem value="suspended">Suspended</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Campaigns Table */}
      <Card className="bg-gray-900 border-gray-800">
        <CardContent className="p-0">
          {loading ? (
            <div className="text-center py-12 text-gray-400">Loading campaigns...</div>
          ) : filteredCampaigns.length === 0 ? (
            <div className="text-center py-12 text-gray-400">No campaigns found</div>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="border-gray-800 bg-gray-800/50">
                    <TableHead className="text-gray-400 w-12"></TableHead>
                    <TableHead className="text-gray-400">ID</TableHead>
                    <TableHead className="text-gray-400">Name</TableHead>
                    <TableHead className="text-gray-400">Owner</TableHead>
                    <TableHead className="text-gray-400">Links</TableHead>
                    <TableHead className="text-gray-400">Clicks</TableHead>
                    <TableHead className="text-gray-400">Status</TableHead>
                    <TableHead className="text-gray-400">Created</TableHead>
                    <TableHead className="text-gray-400">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredCampaigns.map(campaign => (
                    <TableRow key={campaign.id} className="border-gray-800 hover:bg-gray-800/50 transition-colors">
                      <TableCell>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setExpandedId(expandedId === campaign.id ? null : campaign.id)}
                          className="hover:bg-gray-800"
                        >
                          {expandedId === campaign.id ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                        </Button>
                      </TableCell>
                      <TableCell className="text-white">{campaign.id}</TableCell>
                      <TableCell className="text-white font-medium">{campaign.name}</TableCell>
                      <TableCell className="text-gray-400">{campaign.owner}</TableCell>
                      <TableCell className="text-gray-400">{campaign.links_count || 0}</TableCell>
                      <TableCell className="text-gray-400">{campaign.total_clicks || 0}</TableCell>
                      <TableCell>
                        <Badge className={campaign.status === 'active' ? 'bg-green-600' : 'bg-yellow-600'}>
                          {campaign.status}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-gray-400">
                        {campaign.created_at ? new Date(campaign.created_at).toLocaleDateString() : 'N/A'}
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm" className="hover:bg-gray-800">
                              <MoreVertical className="w-4 h-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end" className="bg-gray-800 border-gray-700">
                            <DropdownMenuLabel className="text-gray-300">Actions</DropdownMenuLabel>
                            <DropdownMenuSeparator className="bg-gray-700" />
                            <DropdownMenuItem onClick={() => handleSuspend(campaign.id)} className="text-yellow-400 cursor-pointer">
                              <Shield className="w-4 h-4 mr-2" />
                              {campaign.status === 'suspended' ? 'Activate' : 'Suspend'}
                            </DropdownMenuItem>
                            <DropdownMenuItem onClick={() => handleExport(campaign.id)} className="text-blue-400 cursor-pointer">
                              <Download className="w-4 h-4 mr-2" />
                              Export
                            </DropdownMenuItem>
                            <DropdownMenuItem onClick={() => { setSelectedCampaign(campaign); setShowDeleteDialog(true); }} className="text-red-400 cursor-pointer">
                              <Trash2 className="w-4 h-4 mr-2" />
                              Delete
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Delete Confirmation Dialog */}
      <Dialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <DialogContent className="bg-gray-900 border-gray-800 text-white">
          <DialogHeader>
            <DialogTitle>Confirm Deletion</DialogTitle>
            <DialogDescription className="text-gray-400">
              Are you sure you want to delete campaign "{selectedCampaign?.name}"? This action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowDeleteDialog(false)} className="border-gray-700">
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleDelete} className="bg-red-600 hover:bg-red-700">
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

// ============================================================================
// SECURITY & THREAT MONITORING TAB COMPONENT
// ============================================================================
const SecurityTab = ({ apiCall }) => {
  const [threats, setThreats] = useState([])
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [threatTypeFilter, setThreatTypeFilter] = useState('all')
  const [threatLevelFilter, setThreatLevelFilter] = useState('all')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [threatsData, summaryData] = await Promise.all([
        apiCall('/api/admin/security/threats'),
        apiCall('/api/admin/security/summary')
      ])
      setThreats(Array.isArray(threatsData) ? threatsData : threatsData.items || [])
      setSummary(summaryData)
    } catch (error) {
      toast.error('Failed to load security data')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleBlock = async (threatId) => {
    try {
      await apiCall(`/api/admin/security/threats/${threatId}/block`, { method: 'POST' })
      toast.success('Threat blocked successfully')
      fetchData()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleWhitelist = async (threatId) => {
    try {
      await apiCall(`/api/admin/security/threats/${threatId}/whitelist`, { method: 'POST' })
      toast.success('Threat whitelisted successfully')
      fetchData()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const filteredThreats = threats.filter(threat => {
    const matchesThreatType = threatTypeFilter === 'all' || threat.threat_type === threatTypeFilter
    const matchesThreatLevel = threatLevelFilter === 'all' || threat.threat_level === threatLevelFilter
    return matchesThreatType && matchesThreatLevel
  })

  return (
    <div className="space-y-4">
      {/* Summary Cards */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="bg-gray-900 border-gray-800 hover:border-gray-700 transition-colors">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400 mb-1">Total Threats</p>
                  <p className="text-3xl font-bold text-white">{summary.total_threats || 0}</p>
                </div>
                <AlertTriangle className="w-8 h-8 text-red-500" />
              </div>
            </CardContent>
          </Card>
          <Card className="bg-gray-900 border-gray-800 hover:border-gray-700 transition-colors">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400 mb-1">Blocked IPs</p>
                  <p className="text-3xl font-bold text-white">{summary.blocked_ips || 0}</p>
                </div>
                <Shield className="w-8 h-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>
          <Card className="bg-gray-900 border-gray-800 hover:border-gray-700 transition-colors">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400 mb-1">Whitelisted</p>
                  <p className="text-3xl font-bold text-white">{summary.whitelisted_ips || 0}</p>
                </div>
                <Check className="w-8 h-8 text-green-500" />
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-col md:flex-row gap-4">
        <Select value={threatTypeFilter} onValueChange={setThreatTypeFilter}>
          <SelectTrigger className="w-[180px] bg-gray-900 border-gray-800 text-white">
            <SelectValue placeholder="Threat Type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Types</SelectItem>
            <SelectItem value="proxy">Proxy</SelectItem>
            <SelectItem value="bot">Bot</SelectItem>
            <SelectItem value="rapid_click">Rapid Click</SelectItem>
            <SelectItem value="suspicious">Suspicious</SelectItem>
          </SelectContent>
        </Select>

        <Select value={threatLevelFilter} onValueChange={setThreatLevelFilter}>
          <SelectTrigger className="w-[180px] bg-gray-900 border-gray-800 text-white">
            <SelectValue placeholder="Threat Level" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Levels</SelectItem>
            <SelectItem value="low">Low</SelectItem>
            <SelectItem value="medium">Medium</SelectItem>
            <SelectItem value="high">High</SelectItem>
            <SelectItem value="critical">Critical</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Threats Table */}
      <Card className="bg-gray-900 border-gray-800">
        <CardContent className="p-0">
          {loading ? (
            <div className="text-center py-12 text-gray-400">Loading threats...</div>
          ) : filteredThreats.length === 0 ? (
            <div className="text-center py-12 text-gray-400">No threats found</div>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="border-gray-800 bg-gray-800/50">
                    <TableHead className="text-gray-400">ID</TableHead>
                    <TableHead className="text-gray-400">IP Address</TableHead>
                    <TableHead className="text-gray-400">Type</TableHead>
                    <TableHead className="text-gray-400">Level</TableHead>
                    <TableHead className="text-gray-400">Country</TableHead>
                    <TableHead className="text-gray-400">Status</TableHead>
                    <TableHead className="text-gray-400">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredThreats.map(threat => (
                    <TableRow key={threat.id} className="border-gray-800 hover:bg-gray-800/50 transition-colors">
                      <TableCell className="text-white">{threat.id}</TableCell>
                      <TableCell className="text-white font-mono text-sm">{threat.ip_address}</TableCell>
                      <TableCell className="text-gray-400">{threat.threat_type}</TableCell>
                      <TableCell>
                        <Badge className={
                          threat.threat_level === 'critical' ? 'bg-red-600' :
                          threat.threat_level === 'high' ? 'bg-orange-600' :
                          threat.threat_level === 'medium' ? 'bg-yellow-600' : 'bg-green-600'
                        }>
                          {threat.threat_level}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-gray-400">{threat.country}</TableCell>
                      <TableCell>
                        <Badge className={threat.is_blocked ? 'bg-red-600' : threat.is_whitelisted ? 'bg-green-600' : 'bg-gray-600'}>
                          {threat.is_blocked ? 'Blocked' : threat.is_whitelisted ? 'Whitelisted' : 'Active'}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm" className="hover:bg-gray-800">
                              <MoreVertical className="w-4 h-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end" className="bg-gray-800 border-gray-700">
                            <DropdownMenuLabel className="text-gray-300">Actions</DropdownMenuLabel>
                            <DropdownMenuSeparator className="bg-gray-700" />
                            {!threat.is_blocked && (
                              <DropdownMenuItem onClick={() => handleBlock(threat.id)} className="text-red-400 cursor-pointer">
                                <Shield className="w-4 h-4 mr-2" />
                                Block
                              </DropdownMenuItem>
                            )}
                            {!threat.is_whitelisted && (
                              <DropdownMenuItem onClick={() => handleWhitelist(threat.id)} className="text-green-400 cursor-pointer">
                                <Check className="w-4 h-4 mr-2" />
                                Whitelist
                              </DropdownMenuItem>
                            )}
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

// ============================================================================
// SUBSCRIPTIONS & PAYMENTS TAB COMPONENT
// ============================================================================
const SubscriptionsTab = ({ apiCall }) => {
  const [subscriptions, setSubscriptions] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showApproveDialog, setShowApproveDialog] = useState(false)
  const [showRejectDialog, setShowRejectDialog] = useState(false)
  const [selectedSubscription, setSelectedSubscription] = useState(null)
  const [approvalDuration, setApprovalDuration] = useState('30')
  const [rejectionReason, setRejectionReason] = useState('')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [subsData, statsData] = await Promise.all([
        apiCall('/api/admin/subscriptions/pending'),
        apiCall('/api/admin/subscriptions/stats')
      ])
      setSubscriptions(Array.isArray(subsData) ? subsData : subsData.items || [])
      setStats(statsData)
    } catch (error) {
      toast.error('Failed to load subscriptions')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async () => {
    if (!selectedSubscription) return
    
    try {
      await apiCall(`/api/admin/subscriptions/${selectedSubscription.id}/approve`, {
        method: 'POST',
        body: JSON.stringify({ duration_days: parseInt(approvalDuration) })
      })
      toast.success('Subscription approved successfully')
      setShowApproveDialog(false)
      setSelectedSubscription(null)
      setApprovalDuration('30')
      fetchData()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleReject = async () => {
    if (!selectedSubscription) return
    
    try {
      await apiCall(`/api/admin/subscriptions/${selectedSubscription.id}/reject`, {
        method: 'POST',
        body: JSON.stringify({ reason: rejectionReason })
      })
      toast.success('Subscription rejected successfully')
      setShowRejectDialog(false)
      setSelectedSubscription(null)
      setRejectionReason('')
      fetchData()
    } catch (error) {
      toast.error(error.message)
    }
  }

  return (
    <div className="space-y-4">
      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="bg-gray-900 border-gray-800 hover:border-gray-700 transition-colors">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400 mb-1">Pending Verifications</p>
                  <p className="text-3xl font-bold text-white">{stats.pending || 0}</p>
                </div>
                <Clock className="w-8 h-8 text-yellow-500" />
              </div>
            </CardContent>
          </Card>
          <Card className="bg-gray-900 border-gray-800 hover:border-gray-700 transition-colors">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400 mb-1">Active Subscriptions</p>
                  <p className="text-3xl font-bold text-white">{stats.active || 0}</p>
                </div>
                <Check className="w-8 h-8 text-green-500" />
              </div>
            </CardContent>
          </Card>
          <Card className="bg-gray-900 border-gray-800 hover:border-gray-700 transition-colors">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400 mb-1">Total Revenue</p>
                  <p className="text-3xl font-bold text-white">${stats.total_revenue || 0}</p>
                </div>
                <CreditCard className="w-8 h-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Subscriptions Table */}
      <Card className="bg-gray-900 border-gray-800">
        <CardContent className="p-0">
          {loading ? (
            <div className="text-center py-12 text-gray-400">Loading subscriptions...</div>
          ) : subscriptions.length === 0 ? (
            <div className="text-center py-12 text-gray-400">No subscriptions found</div>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="border-gray-800 bg-gray-800/50">
                    <TableHead className="text-gray-400">ID</TableHead>
                    <TableHead className="text-gray-400">User</TableHead>
                    <TableHead className="text-gray-400">Plan</TableHead>
                    <TableHead className="text-gray-400">Amount</TableHead>
                    <TableHead className="text-gray-400">Method</TableHead>
                    <TableHead className="text-gray-400">Status</TableHead>
                    <TableHead className="text-gray-400">Submitted</TableHead>
                    <TableHead className="text-gray-400">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {subscriptions.map(sub => (
                    <TableRow key={sub.id} className="border-gray-800 hover:bg-gray-800/50 transition-colors">
                      <TableCell className="text-white">{sub.id}</TableCell>
                      <TableCell className="text-white">{sub.user_email}</TableCell>
                      <TableCell className="text-gray-400">{sub.plan_type}</TableCell>
                      <TableCell className="text-gray-400">{sub.amount} {sub.currency}</TableCell>
                      <TableCell className="text-gray-400">{sub.payment_method}</TableCell>
                      <TableCell>
                        <Badge className={sub.status === 'pending' ? 'bg-yellow-600' : 'bg-gray-600'}>
                          {sub.status}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-gray-400">
                        {sub.created_at ? new Date(sub.created_at).toLocaleDateString() : 'N/A'}
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm" className="hover:bg-gray-800">
                              <MoreVertical className="w-4 h-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end" className="bg-gray-800 border-gray-700">
                            <DropdownMenuLabel className="text-gray-300">Actions</DropdownMenuLabel>
                            <DropdownMenuSeparator className="bg-gray-700" />
                            <DropdownMenuItem onClick={() => { setSelectedSubscription(sub); setShowApproveDialog(true); }} className="text-green-400 cursor-pointer">
                              <Check className="w-4 h-4 mr-2" />
                              Approve
                            </DropdownMenuItem>
                            <DropdownMenuItem onClick={() => { setSelectedSubscription(sub); setShowRejectDialog(true); }} className="text-red-400 cursor-pointer">
                              <X className="w-4 h-4 mr-2" />
                              Reject
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Approve Dialog */}
      <Dialog open={showApproveDialog} onOpenChange={setShowApproveDialog}>
        <DialogContent className="bg-gray-900 border-gray-800 text-white">
          <DialogHeader>
            <DialogTitle>Approve Subscription</DialogTitle>
            <DialogDescription className="text-gray-400">
              Approve subscription for {selectedSubscription?.user_email}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label className="text-gray-300">Duration (days)</Label>
              <Input
                type="number"
                value={approvalDuration}
                onChange={(e) => setApprovalDuration(e.target.value)}
                className="bg-gray-800 border-gray-700 text-white mt-1"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowApproveDialog(false)} className="border-gray-700">
              Cancel
            </Button>
            <Button className="bg-green-600 hover:bg-green-700" onClick={handleApprove}>
              Approve
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Reject Dialog */}
      <Dialog open={showRejectDialog} onOpenChange={setShowRejectDialog}>
        <DialogContent className="bg-gray-900 border-gray-800 text-white">
          <DialogHeader>
            <DialogTitle>Reject Subscription</DialogTitle>
            <DialogDescription className="text-gray-400">
              Reject subscription for {selectedSubscription?.user_email}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label className="text-gray-300">Reason</Label>
              <Textarea
                value={rejectionReason}
                onChange={(e) => setRejectionReason(e.target.value)}
                placeholder="Enter rejection reason..."
                className="bg-gray-800 border-gray-700 text-white mt-1"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowRejectDialog(false)} className="border-gray-700">
              Cancel
            </Button>
            <Button className="bg-red-600 hover:bg-red-700" onClick={handleReject}>
              Reject
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

// ============================================================================
// SUPPORT TICKETS TAB COMPONENT
// ============================================================================
const TicketsTab = ({ apiCall }) => {
  const [tickets, setTickets] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState('all')
  const [priorityFilter, setPriorityFilter] = useState('all')
  const [selectedTicket, setSelectedTicket] = useState(null)
  const [showDetailDialog, setShowDetailDialog] = useState(false)
  const [replyMessage, setReplyMessage] = useState('')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [ticketsData, statsData] = await Promise.all([
        apiCall('/api/admin/tickets'),
        apiCall('/api/admin/tickets/stats')
      ])
      setTickets(Array.isArray(ticketsData) ? ticketsData : ticketsData.items || [])
      setStats(statsData)
    } catch (error) {
      toast.error('Failed to load tickets')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleReply = async () => {
    if (!selectedTicket || !replyMessage.trim()) return
    
    try {
      await apiCall(`/api/admin/tickets/${selectedTicket.id}/reply`, {
        method: 'POST',
        body: JSON.stringify({ message: replyMessage })
      })
      toast.success('Reply sent successfully')
      setReplyMessage('')
      fetchData()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleStatusChange = async (ticketId, newStatus) => {
    try {
      await apiCall(`/api/admin/tickets/${ticketId}/status`, {
        method: 'PATCH',
        body: JSON.stringify({ status: newStatus })
      })
      toast.success('Ticket status updated')
      fetchData()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handlePriorityChange = async (ticketId, newPriority) => {
    try {
      await apiCall(`/api/admin/tickets/${ticketId}/priority`, {
        method: 'PATCH',
        body: JSON.stringify({ priority: newPriority })
      })
      toast.success('Ticket priority updated')
      fetchData()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const filteredTickets = tickets.filter(ticket => {
    const matchesStatus = statusFilter === 'all' || ticket.status === statusFilter
    const matchesPriority = priorityFilter === 'all' || ticket.priority === priorityFilter
    return matchesStatus && matchesPriority
  })

  return (
    <div className="space-y-4">
      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="bg-gray-900 border-gray-800 hover:border-gray-700 transition-colors">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400 mb-1">Open Tickets</p>
                  <p className="text-3xl font-bold text-white">{stats.open || 0}</p>
                </div>
                <MessageSquare className="w-8 h-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>
          <Card className="bg-gray-900 border-gray-800 hover:border-gray-700 transition-colors">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400 mb-1">In Progress</p>
                  <p className="text-3xl font-bold text-white">{stats.in_progress || 0}</p>
                </div>
                <Clock className="w-8 h-8 text-yellow-500" />
              </div>
            </CardContent>
          </Card>
          <Card className="bg-gray-900 border-gray-800 hover:border-gray-700 transition-colors">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400 mb-1">Resolved</p>
                  <p className="text-3xl font-bold text-white">{stats.resolved || 0}</p>
                </div>
                <Check className="w-8 h-8 text-green-500" />
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-col md:flex-row gap-4">
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-[140px] bg-gray-900 border-gray-800 text-white">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="open">Open</SelectItem>
            <SelectItem value="in_progress">In Progress</SelectItem>
            <SelectItem value="resolved">Resolved</SelectItem>
          </SelectContent>
        </Select>

        <Select value={priorityFilter} onValueChange={setPriorityFilter}>
          <SelectTrigger className="w-[140px] bg-gray-900 border-gray-800 text-white">
            <SelectValue placeholder="Priority" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Priorities</SelectItem>
            <SelectItem value="low">Low</SelectItem>
            <SelectItem value="medium">Medium</SelectItem>
            <SelectItem value="high">High</SelectItem>
            <SelectItem value="critical">Critical</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Tickets Table */}
      <Card className="bg-gray-900 border-gray-800">
        <CardContent className="p-0">
          {loading ? (
            <div className="text-center py-12 text-gray-400">Loading tickets...</div>
          ) : filteredTickets.length === 0 ? (
            <div className="text-center py-12 text-gray-400">No tickets found</div>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="border-gray-800 bg-gray-800/50">
                    <TableHead className="text-gray-400">ID</TableHead>
                    <TableHead className="text-gray-400">Reference</TableHead>
                    <TableHead className="text-gray-400">User</TableHead>
                    <TableHead className="text-gray-400">Subject</TableHead>
                    <TableHead className="text-gray-400">Status</TableHead>
                    <TableHead className="text-gray-400">Priority</TableHead>
                    <TableHead className="text-gray-400">Created</TableHead>
                    <TableHead className="text-gray-400">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredTickets.map(ticket => (
                    <TableRow key={ticket.id} className="border-gray-800 hover:bg-gray-800/50 transition-colors">
                      <TableCell className="text-white">{ticket.id}</TableCell>
                      <TableCell className="text-white font-mono text-sm">{ticket.ticket_ref}</TableCell>
                      <TableCell className="text-gray-400">{ticket.user_email}</TableCell>
                      <TableCell className="text-white">{ticket.subject}</TableCell>
                      <TableCell>
                        <Badge className={
                          ticket.status === 'resolved' ? 'bg-green-600' :
                          ticket.status === 'in_progress' ? 'bg-blue-600' : 'bg-yellow-600'
                        }>
                          {ticket.status}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Badge className={
                          ticket.priority === 'critical' ? 'bg-red-600' :
                          ticket.priority === 'high' ? 'bg-orange-600' :
                          ticket.priority === 'medium' ? 'bg-yellow-600' : 'bg-green-600'
                        }>
                          {ticket.priority}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-gray-400">
                        {ticket.created_at ? new Date(ticket.created_at).toLocaleDateString() : 'N/A'}
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm" className="hover:bg-gray-800">
                              <MoreVertical className="w-4 h-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end" className="bg-gray-800 border-gray-700">
                            <DropdownMenuLabel className="text-gray-300">Actions</DropdownMenuLabel>
                            <DropdownMenuSeparator className="bg-gray-700" />
                            <DropdownMenuItem onClick={() => { setSelectedTicket(ticket); setShowDetailDialog(true); }} className="text-blue-400 cursor-pointer">
                              <Eye className="w-4 h-4 mr-2" />
                              View Details
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Ticket Detail Dialog */}
      <Dialog open={showDetailDialog} onOpenChange={setShowDetailDialog}>
        <DialogContent className="bg-gray-900 border-gray-800 text-white max-w-2xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{selectedTicket?.subject}</DialogTitle>
            <DialogDescription className="text-gray-400">
              {selectedTicket?.ticket_ref}
            </DialogDescription>
          </DialogHeader>
          
          {selectedTicket && (
            <div className="space-y-4">
              {/* Ticket Info */}
              <div className="grid grid-cols-2 gap-4 p-4 bg-gray-800 rounded">
                <div>
                  <p className="text-sm text-gray-400">Status</p>
                  <Select value={selectedTicket.status} onValueChange={(val) => handleStatusChange(selectedTicket.id, val)}>
                    <SelectTrigger className="bg-gray-700 border-gray-600 text-white mt-1">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="open">Open</SelectItem>
                      <SelectItem value="in_progress">In Progress</SelectItem>
                      <SelectItem value="resolved">Resolved</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Priority</p>
                  <Select value={selectedTicket.priority} onValueChange={(val) => handlePriorityChange(selectedTicket.id, val)}>
                    <SelectTrigger className="bg-gray-700 border-gray-600 text-white mt-1">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="low">Low</SelectItem>
                      <SelectItem value="medium">Medium</SelectItem>
                      <SelectItem value="high">High</SelectItem>
                      <SelectItem value="critical">Critical</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Message */}
              <div className="p-4 bg-gray-800 rounded">
                <p className="text-sm text-gray-400 mb-2">Message</p>
                <p className="text-white">{selectedTicket.message}</p>
              </div>

              {/* Reply Section */}
              <div className="space-y-2">
                <Label className="text-gray-400">Reply</Label>
                <Textarea
                  value={replyMessage}
                  onChange={(e) => setReplyMessage(e.target.value)}
                  placeholder="Type your reply..."
                  className="bg-gray-800 border-gray-700 text-white"
                />
              </div>
            </div>
          )}

          <DialogFooter>
            <Button variant="outline" onClick={() => setShowDetailDialog(false)} className="border-gray-700">
              Close
            </Button>
            <Button className="bg-blue-600 hover:bg-blue-700" onClick={handleReply}>
              Send Reply
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

// ============================================================================
// AUDIT LOGS TAB COMPONENT
// ============================================================================
const AuditLogsTab = ({ apiCall }) => {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [actionFilter, setActionFilter] = useState('all')

  useEffect(() => {
    fetchLogs()
  }, [])

  const fetchLogs = async () => {
    try {
      setLoading(true)
      const data = await apiCall('/api/admin/audit-logs')
      setLogs(Array.isArray(data) ? data : data.items || [])
    } catch (error) {
      toast.error('Failed to load audit logs')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async () => {
    try {
      const data = await apiCall('/api/admin/audit-logs/export')
      const csv = data.csv || data
      const blob = new Blob([csv], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'audit-logs.csv'
      a.click()
      toast.success('Audit logs exported successfully')
    } catch (error) {
      toast.error(error.message)
    }
  }

  const filteredLogs = logs.filter(log => {
    const matchesSearch = log.actor?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         log.action?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesAction = actionFilter === 'all' || log.action === actionFilter
    return matchesSearch && matchesAction
  })

  const uniqueActions = [...new Set(logs.map(log => log.action))]

  return (
    <div className="space-y-4">
      {/* Header Actions */}
      <div className="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
        <div className="flex-1 max-w-md">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <Input
              placeholder="Search logs..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 bg-gray-900 border-gray-800 text-white placeholder-gray-500"
            />
          </div>
        </div>
        
        <div className="flex gap-2">
          <Select value={actionFilter} onValueChange={setActionFilter}>
            <SelectTrigger className="w-[180px] bg-gray-900 border-gray-800 text-white">
              <SelectValue placeholder="Action" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Actions</SelectItem>
              {uniqueActions.map(action => (
                <SelectItem key={action} value={action}>{action}</SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Button
            onClick={handleExport}
            className="bg-green-600 hover:bg-green-700 text-white"
          >
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* Logs Table */}
      <Card className="bg-gray-900 border-gray-800">
        <CardContent className="p-0">
          {loading ? (
            <div className="text-center py-12 text-gray-400">Loading audit logs...</div>
          ) : filteredLogs.length === 0 ? (
            <div className="text-center py-12 text-gray-400">No logs found</div>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="border-gray-800 bg-gray-800/50">
                    <TableHead className="text-gray-400">ID</TableHead>
                    <TableHead className="text-gray-400">Actor</TableHead>
                    <TableHead className="text-gray-400">Action</TableHead>
                    <TableHead className="text-gray-400">Resource</TableHead>
                    <TableHead className="text-gray-400">IP Address</TableHead>
                    <TableHead className="text-gray-400">Status</TableHead>
                    <TableHead className="text-gray-400">Timestamp</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredLogs.map(log => (
                    <TableRow key={log.id} className="border-gray-800 hover:bg-gray-800/50 transition-colors">
                      <TableCell className="text-white">{log.id}</TableCell>
                      <TableCell className="text-white">{log.actor}</TableCell>
                      <TableCell className="text-gray-400">{log.action}</TableCell>
                      <TableCell className="text-gray-400">{log.resource_type}</TableCell>
                      <TableCell className="text-gray-400 font-mono text-sm">{log.ip_address}</TableCell>
                      <TableCell>
                        <Badge className={log.status === 'success' ? 'bg-green-600' : 'bg-red-600'}>
                          {log.status}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-gray-400">
                        {log.created_at ? new Date(log.created_at).toLocaleString() : 'N/A'}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

// ============================================================================
// SETTINGS TAB COMPONENT - WITH DOMAIN MANAGEMENT
// ============================================================================
const SettingsTab = ({ apiCall }) => {
  const [settings, setSettings] = useState({})
  const [domains, setDomains] = useState([])
  const [loading, setLoading] = useState(true)
  const [editingKey, setEditingKey] = useState(null)
  const [editingValue, setEditingValue] = useState('')
  const [showAddDomainDialog, setShowAddDomainDialog] = useState(false)
  const [showDeleteDomainDialog, setShowDeleteDomainDialog] = useState(false)
  const [newDomain, setNewDomain] = useState({ domain: '', description: '' })
  const [selectedDomain, setSelectedDomain] = useState(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [settingsData, domainsData] = await Promise.all([
        apiCall('/api/admin/settings'),
        apiCall('/api/admin/domains').catch(() => ({ items: [] }))
      ])
      setSettings(Array.isArray(settingsData) ? settingsData.reduce((acc, s) => ({ ...acc, [s.setting_key]: s }), {}) : settingsData)
      setDomains(Array.isArray(domainsData) ? domainsData : domainsData.items || [])
    } catch (error) {
      toast.error('Failed to load settings')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleSaveSetting = async (key) => {
    try {
      await apiCall(`/api/admin/settings/${key}`, {
        method: 'PATCH',
        body: JSON.stringify({ setting_value: editingValue })
      })
      toast.success('Setting updated successfully')
      setEditingKey(null)
      setEditingValue('')
      fetchData()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleAddDomain = async () => {
    if (!newDomain.domain) {
      toast.error('Please enter a domain')
      return
    }

    try {
      await apiCall('/api/admin/domains', {
        method: 'POST',
        body: JSON.stringify(newDomain)
      })
      toast.success('Domain added successfully')
      setShowAddDomainDialog(false)
      setNewDomain({ domain: '', description: '' })
      fetchData()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleDeleteDomain = async () => {
    if (!selectedDomain) return

    try {
      await apiCall(`/api/admin/domains/${selectedDomain.id}`, { method: 'DELETE' })
      toast.success('Domain deleted successfully')
      setShowDeleteDomainDialog(false)
      setSelectedDomain(null)
      fetchData()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const handleToggleDomainStatus = async (domainId, currentStatus) => {
    try {
      await apiCall(`/api/admin/domains/${domainId}`, {
        method: 'PATCH',
        body: JSON.stringify({ is_active: !currentStatus })
      })
      toast.success('Domain status updated')
      fetchData()
    } catch (error) {
      toast.error(error.message)
    }
  }

  const settingsArray = Array.isArray(settings) ? settings : Object.values(settings)

  return (
    <div className="space-y-6">
      {/* Domain Management Section */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-white">Domain Management</h2>
            <p className="text-gray-400 text-sm mt-1">Manage custom domains for tracking links (up to 100 domains)</p>
          </div>
          <Button
            onClick={() => setShowAddDomainDialog(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Domain
          </Button>
        </div>

        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-0">
            {loading ? (
              <div className="text-center py-12 text-gray-400">Loading domains...</div>
            ) : domains.length === 0 ? (
              <div className="text-center py-12 text-gray-400">No custom domains configured. Add one to get started.</div>
            ) : (
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow className="border-gray-800 bg-gray-800/50">
                      <TableHead className="text-gray-400">Domain</TableHead>
                      <TableHead className="text-gray-400">Description</TableHead>
                      <TableHead className="text-gray-400">Status</TableHead>
                      <TableHead className="text-gray-400">Usage</TableHead>
                      <TableHead className="text-gray-400">Added</TableHead>
                      <TableHead className="text-gray-400">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {domains.map(domain => (
                      <TableRow key={domain.id} className="border-gray-800 hover:bg-gray-800/50 transition-colors">
                        <TableCell className="text-white font-mono">{domain.domain}</TableCell>
                        <TableCell className="text-gray-400">{domain.description || 'N/A'}</TableCell>
                        <TableCell>
                          <Badge className={domain.is_active ? 'bg-green-600' : 'bg-gray-600'}>
                            {domain.is_active ? 'Active' : 'Inactive'}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-gray-400">{domain.usage_count || 0} links</TableCell>
                        <TableCell className="text-gray-400">
                          {domain.created_at ? new Date(domain.created_at).toLocaleDateString() : 'N/A'}
                        </TableCell>
                        <TableCell>
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button variant="ghost" size="sm" className="hover:bg-gray-800">
                                <MoreVertical className="w-4 h-4" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end" className="bg-gray-800 border-gray-700">
                              <DropdownMenuLabel className="text-gray-300">Actions</DropdownMenuLabel>
                              <DropdownMenuSeparator className="bg-gray-700" />
                              <DropdownMenuItem onClick={() => handleToggleDomainStatus(domain.id, domain.is_active)} className="text-blue-400 cursor-pointer">
                                <Zap className="w-4 h-4 mr-2" />
                                {domain.is_active ? 'Deactivate' : 'Activate'}
                              </DropdownMenuItem>
                              <DropdownMenuItem onClick={() => { setSelectedDomain(domain); setShowDeleteDomainDialog(true); }} className="text-red-400 cursor-pointer">
                                <Trash2 className="w-4 h-4 mr-2" />
                                Delete
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* System Settings Section */}
      <div>
        <h2 className="text-2xl font-bold text-white mb-4">System Settings</h2>
        {loading ? (
          <div className="text-center py-12 text-gray-400">Loading settings...</div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {settingsArray.map(setting => (
              <Card key={setting.setting_key} className="bg-gray-900 border-gray-800 hover:border-gray-700 transition-colors">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h3 className="text-white font-semibold mb-2">{setting.setting_key}</h3>
                      <p className="text-sm text-gray-400 mb-3">{setting.description}</p>
                      {editingKey === setting.setting_key ? (
                        <div className="flex gap-2">
                          <Input
                            value={editingValue}
                            onChange={(e) => setEditingValue(e.target.value)}
                            className="flex-1 bg-gray-800 border-gray-700 text-white"
                          />
                          <Button
                            onClick={() => handleSaveSetting(setting.setting_key)}
                            className="bg-green-600 hover:bg-green-700"
                          >
                            Save
                          </Button>
                          <Button
                            variant="outline"
                            onClick={() => setEditingKey(null)}
                            className="border-gray-700"
                          >
                            Cancel
                          </Button>
                        </div>
                      ) : (
                        <div className="flex items-center justify-between">
                          <p className="text-white font-mono text-sm break-all">{setting.setting_value}</p>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => { setEditingKey(setting.setting_key); setEditingValue(setting.setting_value); }}
                            className="border-gray-700 ml-2"
                          >
                            <Edit className="w-4 h-4 mr-2" />
                            Edit
                          </Button>
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Add Domain Dialog */}
      <Dialog open={showAddDomainDialog} onOpenChange={setShowAddDomainDialog}>
        <DialogContent className="bg-gray-900 border-gray-800 text-white">
          <DialogHeader>
            <DialogTitle>Add New Domain</DialogTitle>
            <DialogDescription className="text-gray-400">
              Add a custom domain for tracking links
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label className="text-gray-300">Domain</Label>
              <Input
                value={newDomain.domain}
                onChange={(e) => setNewDomain({...newDomain, domain: e.target.value})}
                placeholder="e.g., links.example.com"
                className="bg-gray-800 border-gray-700 text-white mt-1"
              />
            </div>
            <div>
              <Label className="text-gray-300">Description (Optional)</Label>
              <Input
                value={newDomain.description}
                onChange={(e) => setNewDomain({...newDomain, description: e.target.value})}
                placeholder="e.g., Main tracking domain"
                className="bg-gray-800 border-gray-700 text-white mt-1"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowAddDomainDialog(false)} className="border-gray-700">
              Cancel
            </Button>
            <Button className="bg-blue-600 hover:bg-blue-700" onClick={handleAddDomain}>
              Add Domain
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Domain Dialog */}
      <Dialog open={showDeleteDomainDialog} onOpenChange={setShowDeleteDomainDialog}>
        <DialogContent className="bg-gray-900 border-gray-800 text-white">
          <DialogHeader>
            <DialogTitle>Confirm Deletion</DialogTitle>
            <DialogDescription className="text-gray-400">
              Are you sure you want to delete domain "{selectedDomain?.domain}"? This action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowDeleteDomainDialog(false)} className="border-gray-700">
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleDeleteDomain} className="bg-red-600 hover:bg-red-700">
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

export default AdminPanelComplete

