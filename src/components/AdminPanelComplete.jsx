import React, { useState, useEffect } from 'react';
import { toast } from 'sonner';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
  Users, FolderKanban, Shield, CreditCard, MessageSquare, FileText, Settings, LayoutDashboard,
  UserCheck, UserX, Trash2, Edit, Eye, MoreVertical, Download, RefreshCw, AlertTriangle,
  Search, Filter, Plus, ChevronDown, ChevronUp, TrendingUp, TrendingDown, Activity
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
  const [loading, setLoading] = useState(false)

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
          <p className="text-gray-400">Comprehensive system administration and monitoring</p>
        </div>

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="w-full justify-start overflow-x-auto bg-gray-900 border-gray-800">
            <TabsTrigger value="dashboard" className="data-[state=active]:bg-blue-600">
              <LayoutDashboard className="w-4 h-4 mr-2" />
              Dashboard
            </TabsTrigger>
            <TabsTrigger value="users" className="data-[state=active]:bg-blue-600">
              <Users className="w-4 h-4 mr-2" />
              Users
            </TabsTrigger>
            <TabsTrigger value="campaigns" className="data-[state=active]:bg-blue-600">
              <FolderKanban className="w-4 h-4 mr-2" />
              Campaigns
            </TabsTrigger>
            <TabsTrigger value="security" className="data-[state=active]:bg-blue-600">
              <Shield className="w-4 h-4 mr-2" />
              Security
            </TabsTrigger>
            <TabsTrigger value="subscriptions" className="data-[state=active]:bg-blue-600">
              <CreditCard className="w-4 h-4 mr-2" />
              Subscriptions
            </TabsTrigger>
            <TabsTrigger value="tickets" className="data-[state=active]:bg-blue-600">
              <MessageSquare className="w-4 h-4 mr-2" />
              Support
            </TabsTrigger>
            <TabsTrigger value="audit" className="data-[state=active]:bg-blue-600">
              <FileText className="w-4 h-4 mr-2" />
              Audit Logs
            </TabsTrigger>
            <TabsTrigger value="settings" className="data-[state=active]:bg-blue-600">
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
    <Card className="bg-gray-900 border-gray-800">
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
          <div className={`p-4 rounded-full ${color}`}>
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
                      <p className="text-xs text-gray-400">{campaign.created_at}</p>
                    </div>
                    <Badge className={campaign.status === 'active' ? 'bg-green-600' : 'bg-gray-600'}>
                      {campaign.status}
                    </Badge>
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
              placeholder="Search users..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 bg-gray-900 border-gray-800 text-white"
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
            className="bg-blue-600 hover:bg-blue-700"
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
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="border-gray-800">
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
                    <TableRow key={user.id} className="border-gray-800">
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
                      <TableCell className="text-gray-400">{user.plan_type}</TableCell>
                      <TableCell className="text-gray-400">
                        {user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm">
                              <MoreVertical className="w-4 h-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuLabel>Actions</DropdownMenuLabel>
                            <DropdownMenuSeparator />
                            {user.status === 'pending' && (
                              <DropdownMenuItem onClick={() => handleApprove(user.id)}>
                                <UserCheck className="w-4 h-4 mr-2" />
                                Approve
                              </DropdownMenuItem>
                            )}
                            <DropdownMenuItem onClick={() => handleSuspend(user.id)}>
                              <UserX className="w-4 h-4 mr-2" />
                              {user.status === 'suspended' ? 'Unsuspend' : 'Suspend'}
                            </DropdownMenuItem>
                            <DropdownMenuItem onClick={() => { setSelectedUser(user); setShowDeleteDialog(true); }}>
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
              Are you sure you want to delete user "{selectedUser?.username}"? This action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowDeleteDialog(false)}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleDelete}>
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

// Placeholder components for other tabs (to be implemented)
const CampaignManagementTab = ({ apiCall }) => <div className="text-white">Campaign Management - Implementation needed</div>
const SecurityTab = ({ apiCall }) => <div className="text-white">Security Monitoring - Implementation needed</div>
const SubscriptionsTab = ({ apiCall }) => <div className="text-white">Subscriptions - Implementation needed</div>
const TicketsTab = ({ apiCall }) => <div className="text-white">Support Tickets - Implementation needed</div>
const AuditLogsTab = ({ apiCall }) => <div className="text-white">Audit Logs - Implementation needed</div>
const SettingsTab = ({ apiCall }) => <div className="text-white">Admin Settings - Implementation needed</div>

export default AdminPanelComplete
