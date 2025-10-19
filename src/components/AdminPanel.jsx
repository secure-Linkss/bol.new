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
  AlertTriangle,
  Plus,
  Search,
  Filter,
  TrendingUp,
  Lock,
  Unlock,
  Mail,
  Phone,
  Calendar,
  Clock,
  CheckCircle,
  AlertCircle,
  XCircle,
  ChevronDown,
  ChevronUp
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
  // State Management
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
  
  // Additional state for enhanced features
  const [searchQuery, setSearchQuery] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const [showSecurityModal, setShowSecurityModal] = useState(false)
  const [showSubscriptionModal, setShowSubscriptionModal] = useState(false)
  const [showSupportModal, setShowSupportModal] = useState(false)
  const [selectedThreat, setSelectedThreat] = useState(null)
  const [selectedSubscription, setSelectedSubscription] = useState(null)
  const [selectedTicket, setSelectedTicket] = useState(null)
  const [expandedRows, setExpandedRows] = useState({})

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
      setError('Failed to load dashboard stats')
    }
  }

  const loadUsers = async () => {
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
    }
  }

  const loadCampaigns = async () => {
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
    }
  }

  const loadAuditLogs = async () => {
    try {
      const response = await fetch('/api/admin/audit-logs', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setAuditLogs(data)
      }
    } catch (error) {
      setError('Failed to load audit logs')
    }
  }

  const deleteUser = async (userId) => {
    try {
      const response = await fetch(`/api/admin/users/${userId}`, {
        method: 'DELETE',
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
    try {
      const response = await fetch('/api/admin/system/delete-all', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
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

  const toggleRowExpansion = (rowId) => {
    setExpandedRows(prev => ({
      ...prev,
      [rowId]: !prev[rowId]
    }))
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

        {/* Main Tabs */}
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
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <Card className="bg-slate-800 border-slate-700">
                    <CardHeader>
                      <CardTitle className="text-white text-sm">Total Users</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-3xl font-bold text-blue-400">{dashboardStats.total_users || 0}</p>
                    </CardContent>
                  </Card>
                  <Card className="bg-slate-800 border-slate-700">
                    <CardHeader>
                      <CardTitle className="text-white text-sm">Active Campaigns</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-3xl font-bold text-green-400">{dashboardStats.active_campaigns || 0}</p>
                    </CardContent>
                  </Card>
                  <Card className="bg-slate-800 border-slate-700">
                    <CardHeader>
                      <CardTitle className="text-white text-sm">Total Clicks</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-3xl font-bold text-purple-400">{dashboardStats.total_clicks || 0}</p>
                    </CardContent>
                  </Card>
                  <Card className="bg-slate-800 border-slate-700">
                    <CardHeader>
                      <CardTitle className="text-white text-sm">Verified Conversions</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-3xl font-bold text-orange-400">{dashboardStats.verified_conversions || 0}</p>
                    </CardContent>
                  </Card>
                </div>
              </>
            )}
          </TabsContent>

          {/* Users Tab */}
          <TabsContent value="users" className="space-y-6">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <div className="flex items-center justify-between flex-wrap gap-4">
                  <CardTitle className="text-white">User Management</CardTitle>
                  <div className="flex gap-2">
                    <Button onClick={() => setShowCreateUserDialog(true)} className="bg-blue-600 hover:bg-blue-700">
                      <Plus className="h-4 w-4 mr-2" />
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
                <div className="space-y-4">
                  <div className="flex gap-2">
                    <Input
                      placeholder="Search users..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="bg-slate-700 border-slate-600 text-white"
                    />
                    <Select value={filterStatus} onValueChange={setFilterStatus}>
                      <SelectTrigger className="bg-slate-700 border-slate-600 text-white w-[150px]">
                        <SelectValue placeholder="Filter by status" />
                      </SelectTrigger>
                      <SelectContent className="bg-slate-700 border-slate-600">
                        <SelectItem value="all">All Status</SelectItem>
                        <SelectItem value="active">Active</SelectItem>
                        <SelectItem value="suspended">Suspended</SelectItem>
                        <SelectItem value="pending">Pending</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="overflow-x-auto">
                    <Table>
                      <TableHeader>
                        <TableRow className="border-slate-700">
                          <TableHead className="text-slate-300">Username</TableHead>
                          <TableHead className="text-slate-300">Email</TableHead>
                          <TableHead className="text-slate-300">Role</TableHead>
                          <TableHead className="text-slate-300">Status</TableHead>
                          <TableHead className="text-slate-300">Created</TableHead>
                          <TableHead className="text-slate-300">Actions</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {users && users.length > 0 ? (
                          users.map(user => (
                            <TableRow key={user.id} className="border-slate-700">
                              <TableCell className="text-white">{user.username}</TableCell>
                              <TableCell className="text-slate-300">{user.email}</TableCell>
                              <TableCell>{getRoleBadge(user.role)}</TableCell>
                              <TableCell>{getStatusBadge(user.status || 'active')}</TableCell>
                              <TableCell className="text-slate-300">{new Date(user.created_at).toLocaleDateString()}</TableCell>
                              <TableCell>
                                <DropdownMenu>
                                  <DropdownMenuTrigger asChild>
                                    <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                                      <MoreVertical className="h-4 w-4" />
                                    </Button>
                                  </DropdownMenuTrigger>
                                  <DropdownMenuContent className="bg-slate-700 border-slate-600">
                                    <DropdownMenuItem className="text-slate-300">
                                      <Edit className="h-4 w-4 mr-2" />
                                      Edit
                                    </DropdownMenuItem>
                                    <DropdownMenuSeparator className="bg-slate-600" />
                                    <DropdownMenuItem className="text-red-400" onClick={() => {
                                      setSelectedUser(user)
                                      setDeleteDialogOpen(true)
                                    }}>
                                      <Trash2 className="h-4 w-4 mr-2" />
                                      Delete
                                    </DropdownMenuItem>
                                  </DropdownMenuContent>
                                </DropdownMenu>
                              </TableCell>
                            </TableRow>
                          ))
                        ) : (
                          <TableRow>
                            <TableCell colSpan="6" className="text-center text-slate-400 py-8">No users found.</TableCell>
                          </TableRow>
                        )}
                      </TableBody>
                    </Table>
                  </div>
                </div>
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
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="border-slate-700">
                        <TableHead className="text-slate-300">Campaign Name</TableHead>
                        <TableHead className="text-slate-300">Status</TableHead>
                        <TableHead className="text-slate-300">Links</TableHead>
                        <TableHead className="text-slate-300">Clicks</TableHead>
                        <TableHead className="text-slate-300">Created</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {campaigns && campaigns.length > 0 ? (
                        campaigns.map(campaign => (
                          <TableRow key={campaign.id} className="border-slate-700">
                            <TableCell className="text-white">{campaign.name}</TableCell>
                            <TableCell>{getStatusBadge(campaign.status)}</TableCell>
                            <TableCell className="text-slate-300">{campaign.link_count || 0}</TableCell>
                            <TableCell className="text-slate-300">{campaign.click_count || 0}</TableCell>
                            <TableCell className="text-slate-300">{new Date(campaign.created_at).toLocaleDateString()}</TableCell>
                          </TableRow>
                        ))
                      ) : (
                        <TableRow>
                          <TableCell colSpan="5" className="text-center text-slate-400 py-8">No campaigns found.</TableCell>
                        </TableRow>
                      )}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Security Tab - Enhanced */}
          <TabsContent value="security" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Active Threats</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-red-400">{securityThreats.filter(t => !t.is_blocked).length}</p>
                </CardContent>
              </Card>
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Blocked Attempts</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-green-400">{securityThreats.filter(t => t.is_blocked).length}</p>
                </CardContent>
              </Card>
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Critical Level</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-orange-400">{securityThreats.filter(t => t.threat_level === 'critical').length}</p>
                </CardContent>
              </Card>
            </div>

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
                        <TableHead className="text-slate-300">IP Address</TableHead>
                        <TableHead className="text-slate-300">Threat Type</TableHead>
                        <TableHead className="text-slate-300">Level</TableHead>
                        <TableHead className="text-slate-300">Blocked</TableHead>
                        <TableHead className="text-slate-300">First Seen</TableHead>
                        <TableHead className="text-slate-300">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {securityThreats && securityThreats.length > 0 ? (
                        securityThreats.map(threat => (
                          <TableRow key={threat.id} className="border-slate-700">
                            <TableCell className="text-white font-mono text-sm">{threat.ip_address}</TableCell>
                            <TableCell className="text-slate-300">{threat.threat_type}</TableCell>
                            <TableCell>
                              <Badge className={threat.threat_level === 'critical' ? 'bg-red-600' : threat.threat_level === 'high' ? 'bg-orange-600' : 'bg-yellow-600'}>
                                {threat.threat_level}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <Badge className={threat.is_blocked ? 'bg-red-600' : 'bg-green-600'}>
                                {threat.is_blocked ? <Lock className="h-3 w-3 mr-1 inline" /> : <Unlock className="h-3 w-3 mr-1 inline" />}
                                {threat.is_blocked ? 'Blocked' : 'Allowed'}
                              </Badge>
                            </TableCell>
                            <TableCell className="text-slate-300 text-sm">{new Date(threat.first_seen).toLocaleString()}</TableCell>
                            <TableCell>
                              <Button size="sm" variant="outline" className="border-slate-600 text-xs" onClick={() => {
                                setSelectedThreat(threat)
                                setShowSecurityModal(true)
                              }}>
                                View Details
                              </Button>
                            </TableCell>
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

          {/* Subscriptions Tab - Enhanced */}
          <TabsContent value="subscriptions" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Total Subscriptions</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-blue-400">{subscriptions.length}</p>
                </CardContent>
              </Card>
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Active</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-green-400">{subscriptions.filter(s => s.is_active).length}</p>
                </CardContent>
              </Card>
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Expiring Soon</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-orange-400">{subscriptions.filter(s => {
                    const expiry = new Date(s.subscription_expiry)
                    const today = new Date()
                    const daysUntilExpiry = Math.floor((expiry - today) / (1000 * 60 * 60 * 24))
                    return daysUntilExpiry <= 7 && daysUntilExpiry > 0
                  }).length}</p>
                </CardContent>
              </Card>
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Expired</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-red-400">{subscriptions.filter(s => {
                    const expiry = new Date(s.subscription_expiry)
                    const today = new Date()
                    return expiry < today
                  }).length}</p>
                </CardContent>
              </Card>
            </div>

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
                        <TableHead className="text-slate-300">User</TableHead>
                        <TableHead className="text-slate-300">Plan Type</TableHead>
                        <TableHead className="text-slate-300">Status</TableHead>
                        <TableHead className="text-slate-300">Expiry Date</TableHead>
                        <TableHead className="text-slate-300">Days Left</TableHead>
                        <TableHead className="text-slate-300">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {subscriptions && subscriptions.length > 0 ? (
                        subscriptions.map(sub => {
                          const expiry = new Date(sub.subscription_expiry)
                          const today = new Date()
                          const daysLeft = Math.floor((expiry - today) / (1000 * 60 * 60 * 24))
                          return (
                            <TableRow key={sub.id} className="border-slate-700">
                              <TableCell className="text-white">{sub.username}</TableCell>
                              <TableCell>
                                <Badge className={sub.plan_type === 'enterprise' ? 'bg-purple-600' : sub.plan_type === 'pro' ? 'bg-blue-600' : 'bg-gray-600'}>
                                  {sub.plan_type}
                                </Badge>
                              </TableCell>
                              <TableCell>
                                <Badge className={sub.is_active ? 'bg-green-600' : 'bg-red-600'}>
                                  {sub.is_active ? <CheckCircle className="h-3 w-3 mr-1 inline" /> : <XCircle className="h-3 w-3 mr-1 inline" />}
                                  {sub.is_active ? 'Active' : 'Inactive'}
                                </Badge>
                              </TableCell>
                              <TableCell className="text-slate-300">{expiry.toLocaleDateString()}</TableCell>
                              <TableCell>
                                <Badge className={daysLeft > 30 ? 'bg-green-600' : daysLeft > 7 ? 'bg-yellow-600' : 'bg-red-600'}>
                                  {daysLeft > 0 ? `${daysLeft}d` : 'Expired'}
                                </Badge>
                              </TableCell>
                              <TableCell>
                                <Button size="sm" variant="outline" className="border-slate-600 text-xs" onClick={() => {
                                  setSelectedSubscription(sub)
                                  setShowSubscriptionModal(true)
                                }}>
                                  Manage
                                </Button>
                              </TableCell>
                            </TableRow>
                          )
                        })
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

          {/* Support Tab - Enhanced */}
          <TabsContent value="support" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Total Tickets</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-blue-400">{supportTickets.length}</p>
                </CardContent>
              </Card>
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Open</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-orange-400">{supportTickets.filter(t => t.status === 'open').length}</p>
                </CardContent>
              </Card>
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-sm">In Progress</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-yellow-400">{supportTickets.filter(t => t.status === 'in_progress').length}</p>
                </CardContent>
              </Card>
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Resolved</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-green-400">{supportTickets.filter(t => t.status === 'resolved').length}</p>
                </CardContent>
              </Card>
            </div>

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
                            <TableCell className="text-white font-mono text-sm">#{ticket.id}</TableCell>
                            <TableCell className="text-slate-300">{ticket.user_email}</TableCell>
                            <TableCell className="text-white">{ticket.subject}</TableCell>
                            <TableCell>
                              <Badge className={ticket.status === 'open' ? 'bg-blue-600' : ticket.status === 'in_progress' ? 'bg-yellow-600' : 'bg-green-600'}>
                                {ticket.status === 'open' ? <AlertCircle className="h-3 w-3 mr-1 inline" /> : ticket.status === 'in_progress' ? <Clock className="h-3 w-3 mr-1 inline" /> : <CheckCircle className="h-3 w-3 mr-1 inline" />}
                                {ticket.status}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <Badge className={ticket.priority === 'high' ? 'bg-red-600' : ticket.priority === 'medium' ? 'bg-orange-600' : 'bg-green-600'}>
                                {ticket.priority}
                              </Badge>
                            </TableCell>
                            <TableCell className="text-slate-300 text-sm">{new Date(ticket.created_at).toLocaleDateString()}</TableCell>
                            <TableCell>
                              <Button size="sm" variant="outline" className="border-slate-600 text-xs" onClick={() => {
                                setSelectedTicket(ticket)
                                setShowSupportModal(true)
                              }}>
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
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="border-slate-700">
                        <TableHead className="text-slate-300">ID</TableHead>
                        <TableHead className="text-slate-300">User ID</TableHead>
                        <TableHead className="text-slate-300">Action</TableHead>
                        <TableHead className="text-slate-300">Timestamp</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {auditLogs.map(log => (
                        <TableRow key={log.id} className="border-slate-700">
                          <TableCell className="text-slate-300">{log.id}</TableCell>
                          <TableCell className="text-slate-300">{log.user_id}</TableCell>
                          <TableCell className="text-white">{log.action}</TableCell>
                          <TableCell className="text-slate-300">{new Date(log.timestamp).toLocaleString()}</TableCell>
                        </TableRow>
                      ))}
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

        {/* Security Threat Details Modal */}
        <Dialog open={showSecurityModal} onOpenChange={setShowSecurityModal}>
          <DialogContent className="bg-slate-800 border-slate-700 max-w-2xl">
            <DialogHeader>
              <DialogTitle className="text-white">Security Threat Details</DialogTitle>
            </DialogHeader>
            {selectedThreat && (
              <div className="space-y-4 py-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className="text-slate-400 text-sm">IP Address</Label>
                    <p className="text-white font-mono">{selectedThreat.ip_address}</p>
                  </div>
                  <div>
                    <Label className="text-slate-400 text-sm">Threat Type</Label>
                    <p className="text-white">{selectedThreat.threat_type}</p>
                  </div>
                  <div>
                    <Label className="text-slate-400 text-sm">Threat Level</Label>
                    <Badge className={selectedThreat.threat_level === 'critical' ? 'bg-red-600' : 'bg-orange-600'}>
                      {selectedThreat.threat_level}
                    </Badge>
                  </div>
                  <div>
                    <Label className="text-slate-400 text-sm">Status</Label>
                    <Badge className={selectedThreat.is_blocked ? 'bg-red-600' : 'bg-green-600'}>
                      {selectedThreat.is_blocked ? 'Blocked' : 'Allowed'}
                    </Badge>
                  </div>
                  <div className="col-span-2">
                    <Label className="text-slate-400 text-sm">First Seen</Label>
                    <p className="text-white">{new Date(selectedThreat.first_seen).toLocaleString()}</p>
                  </div>
                </div>
              </div>
            )}
            <DialogFooter>
              <Button onClick={() => setShowSecurityModal(false)} className="bg-blue-600 hover:bg-blue-700">
                Close
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {/* Subscription Management Modal */}
        <Dialog open={showSubscriptionModal} onOpenChange={setShowSubscriptionModal}>
          <DialogContent className="bg-slate-800 border-slate-700 max-w-2xl">
            <DialogHeader>
              <DialogTitle className="text-white">Subscription Management</DialogTitle>
            </DialogHeader>
            {selectedSubscription && (
              <div className="space-y-4 py-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className="text-slate-400 text-sm">User</Label>
                    <p className="text-white">{selectedSubscription.username}</p>
                  </div>
                  <div>
                    <Label className="text-slate-400 text-sm">Plan Type</Label>
                    <Badge className={selectedSubscription.plan_type === 'enterprise' ? 'bg-purple-600' : 'bg-blue-600'}>
                      {selectedSubscription.plan_type}
                    </Badge>
                  </div>
                  <div>
                    <Label className="text-slate-400 text-sm">Status</Label>
                    <Badge className={selectedSubscription.is_active ? 'bg-green-600' : 'bg-red-600'}>
                      {selectedSubscription.is_active ? 'Active' : 'Inactive'}
                    </Badge>
                  </div>
                  <div>
                    <Label className="text-slate-400 text-sm">Expiry Date</Label>
                    <p className="text-white">{new Date(selectedSubscription.subscription_expiry).toLocaleDateString()}</p>
                  </div>
                </div>
                <div className="space-y-2">
                  <Label className="text-white">Extend Subscription</Label>
                  <Select>
                    <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                      <SelectValue placeholder="Select duration" />
                    </SelectTrigger>
                    <SelectContent className="bg-slate-700 border-slate-600">
                      <SelectItem value="1m">1 Month</SelectItem>
                      <SelectItem value="3m">3 Months</SelectItem>
                      <SelectItem value="6m">6 Months</SelectItem>
                      <SelectItem value="1y">1 Year</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            )}
            <DialogFooter>
              <Button variant="outline" onClick={() => setShowSubscriptionModal(false)} className="border-slate-600">
                Cancel
              </Button>
              <Button className="bg-blue-600 hover:bg-blue-700">
                Update Subscription
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {/* Support Ticket Details Modal */}
        <Dialog open={showSupportModal} onOpenChange={setShowSupportModal}>
          <DialogContent className="bg-slate-800 border-slate-700 max-w-2xl">
            <DialogHeader>
              <DialogTitle className="text-white">Support Ticket Details</DialogTitle>
            </DialogHeader>
            {selectedTicket && (
              <div className="space-y-4 py-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="col-span-2">
                    <Label className="text-slate-400 text-sm">Subject</Label>
                    <p className="text-white font-semibold">{selectedTicket.subject}</p>
                  </div>
                  <div>
                    <Label className="text-slate-400 text-sm">User Email</Label>
                    <p className="text-white">{selectedTicket.user_email}</p>
                  </div>
                  <div>
                    <Label className="text-slate-400 text-sm">Status</Label>
                    <Badge className={selectedTicket.status === 'open' ? 'bg-blue-600' : 'bg-green-600'}>
                      {selectedTicket.status}
                    </Badge>
                  </div>
                  <div>
                    <Label className="text-slate-400 text-sm">Priority</Label>
                    <Badge className={selectedTicket.priority === 'high' ? 'bg-red-600' : 'bg-orange-600'}>
                      {selectedTicket.priority}
                    </Badge>
                  </div>
                  <div>
                    <Label className="text-slate-400 text-sm">Created</Label>
                    <p className="text-white">{new Date(selectedTicket.created_at).toLocaleString()}</p>
                  </div>
                  <div className="col-span-2">
                    <Label className="text-slate-400 text-sm">Description</Label>
                    <Textarea
                      value={selectedTicket.description || ''}
                      readOnly
                      className="bg-slate-700 border-slate-600 text-white resize-none"
                      rows={4}
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <Label className="text-white">Response</Label>
                  <Textarea
                    placeholder="Enter your response..."
                    className="bg-slate-700 border-slate-600 text-white"
                    rows={3}
                  />
                </div>
              </div>
            )}
            <DialogFooter>
              <Button variant="outline" onClick={() => setShowSupportModal(false)} className="border-slate-600">
                Cancel
              </Button>
              <Button className="bg-blue-600 hover:bg-blue-700">
                Send Response
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  )
}

export default AdminPanel

