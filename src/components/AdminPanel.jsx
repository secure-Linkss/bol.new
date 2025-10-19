import { useState, useEffect } from 'react';
import { toast } from 'sonner';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
  Users,
  FolderKanban,
  Shield,
  CreditCard,
  MessageSquare,
  FileText,
  Settings,
  LayoutDashboard,
  UserCheck,
  UserX,
  Trash2,
  Edit,
  Eye,
  MoreVertical,
  Download,
  RefreshCw,
  AlertTriangle
} from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
  DropdownMenuLabel,
} from '@/components/ui/dropdown-menu';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Alert, AlertDescription } from '@/components/ui/alert';

const AdminPanel = () => {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [dashboardStats, setDashboardStats] = useState(null)
  const [users, setUsers] = useState([])
  const [campaigns, setCampaigns] = useState([])
  const [auditLogs, setAuditLogs] = useState([])
  const [loading, setLoading] = useState(false)
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
  const [systemDeleteDialog, setSystemDeleteDialog] = useState(false)
  const [confirmText, setConfirmText] = useState('')
  const [selectedUser, setSelectedUser] = useState(null)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)
  const [showCreateUserDialog, setShowCreateUserDialog] = useState(false)
  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    password: '',
    role: 'member',
    status: 'active'
  })
  const [securityThreats, setSecurityThreats] = useState([])
  const [subscriptions, setSubscriptions] = useState([])
  const [supportTickets, setSupportTickets] = useState([])

  useEffect(() => {
    loadDashboardStats()
  }, [])

  useEffect(() => {
    if (activeTab === 'users') {
      loadUsers()
    } else if (activeTab === 'campaigns') {
      loadCampaigns()
    } else if (activeTab === 'audit') {
      loadAuditLogs()
    } else if (activeTab === 'security') {
      loadSecurityThreats()
    } else if (activeTab === 'subscriptions') {
      loadSubscriptions()
    } else if (activeTab === 'support') {
      loadSupportTickets()
    }
  }, [activeTab])

  const loadDashboardStats = async () => {
    try {
      const response = await fetch('/api/admin/dashboard/stats', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setDashboardStats(data)
      }
    } catch (error) {
      console.error('Error loading dashboard stats:', error)
    }
  }

  const loadUsers = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/admin/users', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setUsers(data)
      }
    } catch (error) {
      setError('Failed to load users')
    } finally {
      setLoading(false)
    }
  }

  const loadCampaigns = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/admin/campaigns', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setCampaigns(data)
      }
    } catch (error) {
      setError('Failed to load campaigns')
    } finally {
      setLoading(false)
    }
  }

  const loadAuditLogs = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/admin/audit-logs', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setAuditLogs(data.logs)
      }
    } catch (error) {
      setError('Failed to load audit logs')
    } finally {
      setLoading(false)
    }
  }

  const approveUser = async (userId) => {
    try {
      const response = await fetch(`/api/admin/users/${userId}/approve`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        setSuccess('User approved successfully')
        loadUsers()
      } else {
        setError('Failed to approve user')
      }
    } catch (error) {
      setError('Error approving user')
    }
  }

  const suspendUser = async (userId) => {
    try {
      const response = await fetch(`/api/admin/users/${userId}/suspend`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        setSuccess('User suspended successfully')
        loadUsers()
      } else {
        setError('Failed to suspend user')
      }
    } catch (error) {
      setError('Error suspending user')
    }
  }

  const deleteUser = async (userId) => {
    try {
      const response = await fetch(`/api/admin/users/${userId}/delete`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        setSuccess('User deleted successfully')
        setDeleteDialogOpen(false)
        loadUsers()
      } else {
        const data = await response.json()
        setError(data.error || 'Failed to delete user')
      }
    } catch (error) {
      setError('Error deleting user')
    }
  }

  const deleteAllSystemData = async () => {
    if (confirmText !== 'DELETE_ALL_DATA') {
      setError('Please type DELETE_ALL_DATA to confirm')
      return
    }

    try {
      const response = await fetch('/api/admin/system/delete-all', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ confirm: 'DELETE_ALL_DATA' })
      })

      if (response.ok) {
        setSuccess('All system data deleted successfully')
        setSystemDeleteDialog(false)
        setConfirmText('')
        loadDashboardStats()
      } else {
        const data = await response.json()
        setError(data.error || 'Failed to delete system data')
      }
    } catch (error) {
      setError('Error deleting system data')
    }
  }

  const createUser = async () => {
    if (!newUser.username || !newUser.email || !newUser.password) {
      setError('Please fill in all required fields')
      return
    }

    try {
      const response = await fetch('/api/admin/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(newUser)
      })

      if (response.ok) {
        setSuccess('User created successfully')
        setShowCreateUserDialog(false)
        setNewUser({
          username: '',
          email: '',
          password: '',
          role: 'member',
          status: 'active'
        })
        loadUsers()
      } else {
        const data = await response.json()
        setError(data.error || 'Failed to create user')
      }
    } catch (error) {
      setError('Error creating user')
    }
  }

  const exportAuditLogs = async () => {
    try {
      const response = await fetch('/api/admin/audit-logs/export', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'audit_logs.csv'
        a.click()
        setSuccess('Audit logs exported successfully')
      }
    } catch (error) {
      setError('Failed to export audit logs')
    }
  }

  const getRoleBadge = (role) => {
    const colors = {
      'main_admin': 'bg-purple-500',
      'assistant_admin': 'bg-blue-500',
      'admin': 'bg-blue-400',
      'member': 'bg-gray-500'
    }
    return <Badge className={colors[role] || 'bg-gray-500'}>{role}</Badge>
  }

  const getStatusBadge = (status) => {
    const colors = {
      'pending': 'bg-yellow-500',
      'active': 'bg-green-500',
      'suspended': 'bg-red-500',
      'expired': 'bg-orange-500'
    }
    return <Badge className={colors[status] || 'bg-gray-500'}>{status}</Badge>
  }

  const loadSecurityThreats = async () => {
    try {
      const response = await fetch('/api/admin/security/threats', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setSecurityThreats(data.threats || [])
      }
    } catch (error) {
      setError('Failed to load security threats')
    }
  }

  const loadSubscriptions = async () => {
    try {
      const response = await fetch('/api/admin/subscriptions', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setSubscriptions(data.subscriptions || [])
      }
    } catch (error) {
      setError('Failed to load subscriptions')
    }
  }

  const loadSupportTickets = async () => {
    try {
      const response = await fetch('/api/admin/support/tickets', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setSupportTickets(data.tickets || [])
      }
    } catch (error) {
      setError('Failed to load support tickets')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Admin Panel</h1>
          <p className="text-slate-400">Enterprise-grade administration dashboard</p>
        </div>

        {/* Alerts */}
        {error && (
          <Alert className="mb-4 border-red-500 bg-red-500/10">
            <AlertTriangle className="h-4 w-4 text-red-500" />
            <AlertDescription className="text-red-400">{error}</AlertDescription>
          </Alert>
        )}

        {success && (
          <Alert className="mb-4 border-green-500 bg-green-500/10">
            <AlertDescription className="text-green-400">{success}</AlertDescription>
          </Alert>
        )}

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <div className="overflow-x-auto scrollbar-hide">
            <TabsList className="bg-slate-800 border-slate-700 p-1 flex w-max min-w-full gap-1 md:grid md:grid-cols-8 md:w-full">
              <TabsTrigger value="dashboard" className="data-[state=active]:bg-slate-700 flex items-center justify-center px-2 py-2 text-xs md:text-sm whitespace-nowrap min-w-[80px] md:min-w-0">
                <LayoutDashboard className="h-4 w-4 mr-1 md:mr-2" />
                <span className="hidden sm:inline">Dashboard</span>
                <span className="sm:hidden">Dash</span>
              </TabsTrigger>
              <TabsTrigger value="users" className="data-[state=active]:bg-slate-700 flex items-center justify-center px-2 py-2 text-xs md:text-sm whitespace-nowrap min-w-[80px] md:min-w-0">
                <Users className="h-4 w-4 mr-1 md:mr-2" />
                <span className="hidden sm:inline">Users</span>
                <span className="sm:hidden">Users</span>
              </TabsTrigger>
              <TabsTrigger value="campaigns" className="data-[state=active]:bg-slate-700 flex items-center justify-center px-2 py-2 text-xs md:text-sm whitespace-nowrap min-w-[80px] md:min-w-0">
                <FolderKanban className="h-4 w-4 mr-1 md:mr-2" />
                <span className="hidden sm:inline">Campaigns</span>
                <span className="sm:hidden">Camp</span>
              </TabsTrigger>
              <TabsTrigger value="security" className="data-[state=active]:bg-slate-700 flex items-center justify-center px-2 py-2 text-xs md:text-sm whitespace-nowrap min-w-[80px] md:min-w-0">
                <Shield className="h-4 w-4 mr-1 md:mr-2" />
                <span className="hidden sm:inline">Security</span>
                <span className="sm:hidden">Sec</span>
              </TabsTrigger>
              <TabsTrigger value="subscriptions" className="data-[state=active]:bg-slate-700 flex items-center justify-center px-2 py-2 text-xs md:text-sm whitespace-nowrap min-w-[80px] md:min-w-0">
                <CreditCard className="h-4 w-4 mr-1 md:mr-2" />
                <span className="hidden sm:inline">Subscriptions</span>
                <span className="sm:hidden">Subs</span>
              </TabsTrigger>
              <TabsTrigger value="support" className="data-[state=active]:bg-slate-700 flex items-center justify-center px-2 py-2 text-xs md:text-sm whitespace-nowrap min-w-[80px] md:min-w-0">
                <MessageSquare className="h-4 w-4 mr-1 md:mr-2" />
                <span className="hidden sm:inline">Support</span>
                <span className="sm:hidden">Supp</span>
              </TabsTrigger>
              <TabsTrigger value="audit" className="data-[state=active]:bg-slate-700 flex items-center justify-center px-2 py-2 text-xs md:text-sm whitespace-nowrap min-w-[80px] md:min-w-0">
                <FileText className="h-4 w-4 mr-1 md:mr-2" />
                <span className="hidden sm:inline">Audit</span>
                <span className="sm:hidden">Audit</span>
              </TabsTrigger>
              <TabsTrigger value="settings" className="data-[state=active]:bg-slate-700 flex items-center justify-center px-2 py-2 text-xs md:text-sm whitespace-nowrap min-w-[80px] md:min-w-0">
                <Settings className="h-4 w-4 mr-1 md:mr-2" />
                <span className="hidden sm:inline">Settings</span>
                <span className="sm:hidden">Set</span>
              </TabsTrigger>
            </TabsList>
          </div>

          {/* Dashboard Tab */}
          <TabsContent value="dashboard" className="space-y-6">
            {dashboardStats && (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <Card className="bg-slate-800 border-slate-700">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-white text-sm font-medium">Total Users</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-3xl font-bold text-white">{dashboardStats.users.total}</div>
                      <div className="mt-2 space-y-1">
                        <div className="text-xs text-slate-400">
                          Active: <span className="text-green-400">{dashboardStats.users.active}</span>
                        </div>
                        <div className="text-xs text-slate-400">
                          Pending: <span className="text-yellow-400">{dashboardStats.users.pending}</span>
                        </div>
                        <div className="text-xs text-slate-400">
                          Suspended: <span className="text-red-400">{dashboardStats.users.suspended}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-slate-800 border-slate-700">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-white text-sm font-medium">Campaigns</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-3xl font-bold text-white">{dashboardStats.campaigns.total}</div>
                      <div className="mt-2">
                        <div className="text-xs text-slate-400">
                          Active: <span className="text-green-400">{dashboardStats.campaigns.active}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-slate-800 border-slate-700">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-white text-sm font-medium">Links</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-3xl font-bold text-white">{dashboardStats.links.total}</div>
                      <div className="mt-2">
                        <div className="text-xs text-slate-400">
                          Active: <span className="text-green-400">{dashboardStats.links.active}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-slate-800 border-slate-700">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-white text-sm font-medium">Events</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-3xl font-bold text-white">{dashboardStats.events.total}</div>
                      <div className="mt-2">
                        <div className="text-xs text-slate-400">
                          Today: <span className="text-blue-400">{dashboardStats.events.today}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>

                {/* Recent Activity */}
                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-white">Recent Activity</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <h3 className="text-sm font-medium text-slate-300">Recent Users</h3>
                      <div className="space-y-2">
                        {dashboardStats.recent_users.map(user => (
                          <div key={user.id} className="flex items-center justify-between p-2 bg-slate-700/50 rounded">
                            <div>
                              <span className="text-white font-medium">{user.username}</span>
                              <span className="text-slate-400 text-sm ml-2">{user.email}</span>
                            </div>
                            {getRoleBadge(user.role)}
                          </div>
                        ))}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </>
            )}
          </TabsContent>

          {/* Users Tab */}
          <TabsContent value="users" className="space-y-6">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-white">User Management</CardTitle>
                  <div className="flex gap-2">
                    <Button onClick={() => setShowCreateUserDialog(true)} size="sm" variant="default" className="bg-blue-600 hover:bg-blue-700">
                      <Users className="h-4 w-4 mr-2" />
                      Create User
                    </Button>
                    <Button onClick={loadUsers} size="sm" variant="outline" className="border-slate-600">
                      <RefreshCw className="h-4 w-4 mr-2" />
                      Refresh
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="text-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                    <p className="text-slate-400 mt-2">Loading users...</p>
                  </div>
                ) : users.length === 0 ? (
                  <div className="text-center py-8">
                    <p className="text-slate-400">No users found.</p>
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <Table>
                      <TableHeader>
                        <TableRow className="border-slate-700">
                          <TableHead className="text-slate-300">USER</TableHead>
                          <TableHead className="text-slate-300">ROLE</TableHead>
                          <TableHead className="text-slate-300">STATUS</TableHead>
                          <TableHead className="text-slate-300">CAMPAIGNS</TableHead>
                          <TableHead className="text-slate-300">LAST LOGIN</TableHead>
                          <TableHead className="text-slate-300">ACTIONS</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {users.map(user => (
                          <TableRow key={user.id} className="border-slate-700 hover:bg-slate-700/50">
                            <TableCell className="text-white">
                              <div className="flex items-center gap-3">
                                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                                  <span className="text-white text-sm font-medium">
                                    {user.username?.charAt(0)?.toUpperCase() || 'U'}
                                  </span>
                                </div>
                                <div>
                                  <div className="font-medium">{user.username}</div>
                                  <div className="text-sm text-slate-400">{user.email}</div>
                                </div>
                              </div>
                            </TableCell>
                            <TableCell>{getRoleBadge(user.role)}</TableCell>
                            <TableCell>{getStatusBadge(user.status || 'active')}</TableCell>
                            <TableCell className="text-slate-300">
                              <div className="text-center">
                                <div className="text-lg font-semibold">{user.campaign_count || 0}</div>
                                <div className="text-xs text-slate-400">campaigns</div>
                              </div>
                            </TableCell>
                            <TableCell className="text-slate-300">
                              {user.last_login ? new Date(user.last_login).toLocaleDateString() : 'Never'}
                            </TableCell>
                            <TableCell>
                            <DropdownMenu>
                              <DropdownMenuTrigger asChild>
                                <Button variant="ghost" className="h-8 w-8 p-0">
                                  <MoreVertical className="h-4 w-4" />
                                </Button>
                              </DropdownMenuTrigger>
                              <DropdownMenuContent align="end" className="bg-slate-800 border-slate-700 text-white">
                                <DropdownMenuItem onClick={() => approveUser(user.id)} className="hover:bg-slate-700">
                                  <UserCheck className="mr-2 h-4 w-4" />
                                  Approve
                                </DropdownMenuItem>
                                <DropdownMenuItem onClick={() => suspendUser(user.id)} className="hover:bg-slate-700">
                                  <UserX className="mr-2 h-4 w-4" />
                                  Suspend
                                </DropdownMenuItem>
                                <DropdownMenuSeparator className="bg-slate-700" />
                                <DropdownMenuItem
                                  onClick={() => {
                                    setSelectedUser(user)
                                    setDeleteDialogOpen(true)
                                  }}
                                  className="text-red-400 hover:bg-red-500/10"
                                >
                                  <Trash2 className="mr-2 h-4 w-4" />
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
          </TabsContent>

          {/* Campaigns Tab */}
          <TabsContent value="campaigns" className="space-y-6">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-white">Campaign Management</CardTitle>
                  <Button onClick={loadCampaigns} size="sm" variant="outline" className="border-slate-600">
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Refresh
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="text-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                    <p className="text-slate-400 mt-2">Loading campaigns...</p>
                  </div>
                ) : campaigns.length === 0 ? (
                  <div className="text-center py-8">
                    <p className="text-slate-400">No campaigns found.</p>
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <Table>
                      <TableHeader>
                        <TableRow className="border-slate-700">
                          <TableHead className="text-slate-300">CAMPAIGN</TableHead>
                          <TableHead className="text-slate-300">USER</TableHead>
                          <TableHead className="text-slate-300">STATUS</TableHead>
                          <TableHead className="text-slate-300">CLICKS</TableHead>
                          <TableHead className="text-slate-300">CREATED</TableHead>
                          <TableHead className="text-slate-300">ACTIONS</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {campaigns.map(campaign => (
                          <TableRow key={campaign.id} className="border-slate-700 hover:bg-slate-700/50">
                            <TableCell className="text-white">
                              <div className="flex items-center gap-3">
                                <div className="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center">
                                  <span className="text-white text-sm font-medium">
                                    {campaign.name?.charAt(0)?.toUpperCase() || 'C'}
                                  </span>
                                </div>
                                <div>
                                  <div className="font-medium">{campaign.name || 'Unnamed Campaign'}</div>
                                  <div className="text-sm text-slate-400">ID: {campaign.id}</div>
                                </div>
                              </div>
                            </TableCell>
                            <TableCell className="text-slate-300">
                              <div>
                                <div className="font-medium">User #{campaign.user_id}</div>
                                <div className="text-sm text-slate-400">Campaign Owner</div>
                              </div>
                            </TableCell>
                            <TableCell>
                              <Badge className={campaign.is_active ? 'bg-green-600 text-white' : 'bg-gray-600 text-white'}>
                                {campaign.is_active ? 'Active' : 'Inactive'}
                              </Badge>
                            </TableCell>
                            <TableCell className="text-slate-300">
                              <div className="text-center">
                                <div className="text-lg font-semibold">{campaign.click_count || 0}</div>
                                <div className="text-xs text-slate-400">total clicks</div>
                              </div>
                            </TableCell>
                            <TableCell className="text-slate-300">
                              {campaign.created_at ? new Date(campaign.created_at).toLocaleDateString() : 'N/A'}
                            </TableCell>
                            <TableCell>
                              <div className="flex items-center gap-2">
                                <Button variant="outline" size="sm" className="border-slate-600">
                                  <Eye className="h-4 w-4" />
                                </Button>
                                <Button variant="outline" size="sm" className="border-slate-600">
                                  <Edit className="h-4 w-4" />
                                </Button>
                                <Button variant="outline" size="sm" className="border-red-600 text-red-400">
                                  <Trash2 className="h-4 w-4" />
                                </Button>
                              </div>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Audit Logs Tab */}
          <TabsContent value="audit" className="space-y-6">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-white">Audit Logs</CardTitle>
                  <Button onClick={exportAuditLogs} size="sm" variant="outline" className="border-slate-600">
                    <Download className="h-4 w-4 mr-2" />
                    Export CSV
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="text-slate-300">ID</TableHead>
                      <TableHead className="text-slate-300">User ID</TableHead>
                      <TableHead className="text-slate-300">Action</TableHead>
                      <TableHead className="text-slate-300">Timestamp</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {auditLogs.map(log => (
                      <TableRow key={log.id}>
                        <TableCell className="text-slate-300">{log.id}</TableCell>
                        <TableCell className="text-slate-300">{log.user_id}</TableCell>
                        <TableCell className="text-white">{log.action}</TableCell>
                        <TableCell className="text-slate-300">{new Date(log.timestamp).toLocaleString()}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Security Tab */}
          <TabsContent value="security" className="space-y-6">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-white">Security Threats</CardTitle>
                  <Button onClick={() => loadSecurityThreats()} size="sm" variant="outline" className="border-slate-600">
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Refresh
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="border-slate-700">
                        <TableHead className="text-slate-300">ID</TableHead>
                        <TableHead className="text-slate-300">IP Address</TableHead>
                        <TableHead className="text-slate-300">Threat Type</TableHead>
                        <TableHead className="text-slate-300">Level</TableHead>
                        <TableHead className="text-slate-300">Blocked</TableHead>
                        <TableHead className="text-slate-300">Timestamp</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {securityThreats && securityThreats.length > 0 ? (
                        securityThreats.map(threat => (
                          <TableRow key={threat.id} className="border-slate-700">
                            <TableCell className="text-slate-300">{threat.id}</TableCell>
                            <TableCell className="text-slate-300">{threat.ip_address}</TableCell>
                            <TableCell className="text-white">{threat.threat_type}</TableCell>
                            <TableCell>
                              <Badge className={threat.threat_level === 'critical' ? 'bg-red-600' : threat.threat_level === 'high' ? 'bg-orange-600' : 'bg-yellow-600'}>
                                {threat.threat_level}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <Badge className={threat.is_blocked ? 'bg-red-600' : 'bg-green-600'}>
                                {threat.is_blocked ? 'Blocked' : 'Allowed'}
                              </Badge>
                            </TableCell>
                            <TableCell className="text-slate-300">{new Date(threat.first_seen).toLocaleString()}</TableCell>
                          </TableRow>
                        ))
                      ) : (
                        <TableRow>
                          <TableCell colSpan="6" className="text-center text-slate-400 py-8">No security threats detected.</TableCell>
                        </TableRow>
                      )}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Subscriptions Tab */}
          <TabsContent value="subscriptions" className="space-y-6">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-white">Subscription Management</CardTitle>
                  <Button onClick={() => loadSubscriptions()} size="sm" variant="outline" className="border-slate-600">
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Refresh
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="border-slate-700">
                        <TableHead className="text-slate-300">User ID</TableHead>
                        <TableHead className="text-slate-300">Username</TableHead>
                        <TableHead className="text-slate-300">Plan Type</TableHead>
                        <TableHead className="text-slate-300">Status</TableHead>
                        <TableHead className="text-slate-300">Expiry Date</TableHead>
                        <TableHead className="text-slate-300">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {subscriptions && subscriptions.length > 0 ? (
                        subscriptions.map(sub => (
                          <TableRow key={sub.id} className="border-slate-700">
                            <TableCell className="text-slate-300">{sub.user_id}</TableCell>
                            <TableCell className="text-white">{sub.username}</TableCell>
                            <TableCell>
                              <Badge className={sub.plan_type === 'enterprise' ? 'bg-purple-600' : sub.plan_type === 'pro' ? 'bg-blue-600' : 'bg-gray-600'}>
                                {sub.plan_type}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <Badge className={sub.is_active ? 'bg-green-600' : 'bg-red-600'}>
                                {sub.is_active ? 'Active' : 'Inactive'}
                              </Badge>
                            </TableCell>
                            <TableCell className="text-slate-300">{sub.subscription_expiry ? new Date(sub.subscription_expiry).toLocaleDateString() : 'N/A'}</TableCell>
                            <TableCell>
                              <Button size="sm" variant="outline" className="border-slate-600 text-xs">
                                Edit
                              </Button>
                            </TableCell>
                          </TableRow>
                        ))
                      ) : (
                        <TableRow>
                          <TableCell colSpan="6" className="text-center text-slate-400 py-8">No subscriptions found.</TableCell>
                        </TableRow>
                      )}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Support Tab */}
          <TabsContent value="support" className="space-y-6">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-white">Support Tickets</CardTitle>
                  <Button onClick={() => loadSupportTickets()} size="sm" variant="outline" className="border-slate-600">
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Refresh
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="border-slate-700">
                        <TableHead className="text-slate-300">Ticket ID</TableHead>
                        <TableHead className="text-slate-300">User</TableHead>
                        <TableHead className="text-slate-300">Subject</TableHead>
                        <TableHead className="text-slate-300">Status</TableHead>
                        <TableHead className="text-slate-300">Priority</TableHead>
                        <TableHead className="text-slate-300">Created</TableHead>
                        <TableHead className="text-slate-300">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {supportTickets && supportTickets.length > 0 ? (
                        supportTickets.map(ticket => (
                          <TableRow key={ticket.id} className="border-slate-700">
                            <TableCell className="text-slate-300">{ticket.id}</TableCell>
                            <TableCell className="text-white">{ticket.user_email}</TableCell>
                            <TableCell className="text-slate-300">{ticket.subject}</TableCell>
                            <TableCell>
                              <Badge className={ticket.status === 'open' ? 'bg-blue-600' : ticket.status === 'in_progress' ? 'bg-yellow-600' : 'bg-green-600'}>
                                {ticket.status}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <Badge className={ticket.priority === 'high' ? 'bg-red-600' : ticket.priority === 'medium' ? 'bg-orange-600' : 'bg-green-600'}>
                                {ticket.priority}
                              </Badge>
                            </TableCell>
                            <TableCell className="text-slate-300">{new Date(ticket.created_at).toLocaleDateString()}</TableCell>
                            <TableCell>
                              <Button size="sm" variant="outline" className="border-slate-600 text-xs">
                                View
                              </Button>
                            </TableCell>
                          </TableRow>
                        ))
                      ) : (
                        <TableRow>
                          <TableCell colSpan="7" className="text-center text-slate-400 py-8">No support tickets found.</TableCell>
                        </TableRow>
                      )}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Settings Tab */}
          <TabsContent value="settings" className="space-y-6">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">System Settings</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-slate-700/50 rounded-lg">
                    <div>
                      <h3 className="text-white font-medium">Delete All System Data</h3>
                      <p className="text-slate-400 text-sm">This will permanently delete all data. This action cannot be undone.</p>
                    </div>
                    <Button
                      variant="destructive"
                      onClick={() => setSystemDeleteDialog(true)}
                      className="bg-red-600 hover:bg-red-700"
                    >
                      <Trash2 className="h-4 w-4 mr-2" />
                      Delete All System Data
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Delete User Dialog */}
        <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
          <DialogContent className="bg-slate-800 border-slate-700">
            <DialogHeader>
              <DialogTitle className="text-white">Confirm Deletion</DialogTitle>
              <DialogDescription className="text-slate-400">
                Are you sure you want to delete user {selectedUser?.username}? This action cannot be undone.
              </DialogDescription>
            </DialogHeader>
            <DialogFooter>
              <Button variant="outline" onClick={() => setDeleteDialogOpen(false)} className="border-slate-600">
                Cancel
              </Button>
              <Button
                variant="destructive"
                onClick={() => selectedUser && deleteUser(selectedUser.id)}
                className="bg-red-600 hover:bg-red-700"
              >
                Delete
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {/* System Delete Dialog */}
        <Dialog open={systemDeleteDialog} onOpenChange={setSystemDeleteDialog}>
          <DialogContent className="bg-slate-800 border-slate-700">
            <DialogHeader>
              <DialogTitle className="text-white">Confirm System Data Deletion</DialogTitle>
              <DialogDescription className="text-slate-400">
                This will permanently delete ALL system data except the main admin account. This action CANNOT be undone.
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label htmlFor="confirm" className="text-white">
                  Type <span className="font-mono text-red-400">DELETE_ALL_DATA</span> to confirm
                </Label>
                <Input
                  id="confirm"
                  value={confirmText}
                  onChange={(e) => setConfirmText(e.target.value)}
                  placeholder="DELETE_ALL_DATA"
                  className="bg-slate-700 border-slate-600 text-white"
                />
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => {
                setSystemDeleteDialog(false)
                setConfirmText('')
              }} className="border-slate-600">
                Cancel
              </Button>
              <Button
                variant="destructive"
                onClick={deleteAllSystemData}
                disabled={confirmText !== 'DELETE_ALL_DATA'}
                className="bg-red-600 hover:bg-red-700"
              >
                Delete All Data
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {/* Create User Dialog */}
        <Dialog open={showCreateUserDialog} onOpenChange={setShowCreateUserDialog}>
          <DialogContent className="bg-slate-800 border-slate-700">
            <DialogHeader>
              <DialogTitle className="text-white">Create New User</DialogTitle>
              <DialogDescription className="text-slate-400">
                Add a new user to the system with specified role and permissions.
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label htmlFor="username" className="text-white">Username</Label>
                <Input
                  id="username"
                  value={newUser.username}
                  onChange={(e) => setNewUser({...newUser, username: e.target.value})}
                  placeholder="Enter username"
                  className="bg-slate-700 border-slate-600 text-white"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email" className="text-white">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={newUser.email}
                  onChange={(e) => setNewUser({...newUser, email: e.target.value})}
                  placeholder="Enter email address"
                  className="bg-slate-700 border-slate-600 text-white"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password" className="text-white">Password</Label>
                <Input
                  id="password"
                  type="password"
                  value={newUser.password}
                  onChange={(e) => setNewUser({...newUser, password: e.target.value})}
                  placeholder="Enter password"
                  className="bg-slate-700 border-slate-600 text-white"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="role" className="text-white">Role</Label>
                <Select value={newUser.role} onValueChange={(value) => setNewUser({...newUser, role: value})}>
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue placeholder="Select role" />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    <SelectItem value="member">Member</SelectItem>
                    <SelectItem value="admin">Admin</SelectItem>
                    <SelectItem value="main_admin">Main Admin</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="status" className="text-white">Status</Label>
                <Select value={newUser.status} onValueChange={(value) => setNewUser({...newUser, status: value})}>
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue placeholder="Select status" />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    <SelectItem value="active">Active</SelectItem>
                    <SelectItem value="pending">Pending</SelectItem>
                    <SelectItem value="suspended">Suspended</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => {
                setShowCreateUserDialog(false)
                setNewUser({
                  username: '',
                  email: '',
                  password: '',
                  role: 'member',
                  status: 'active'
                })
              }} className="border-slate-600">
                Cancel
              </Button>
              <Button
                onClick={createUser}
                className="bg-blue-600 hover:bg-blue-700"
              >
                Create User
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  )
}

export default AdminPanel
