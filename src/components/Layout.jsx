import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import {
  LayoutDashboard,
  Link2,
  Activity,
  Target,
  BarChart3,
  Globe,
  Shield,
  Settings,
  Scissors,
  Bell,
  LogOut,
  User,
  Menu,
  X
} from 'lucide-react'
import Logo from './Logo'

const Layout = ({ children, user, onLogout }) => {
  const location = useLocation()
  const navigate = useNavigate()
  const [notifications, setNotifications] = useState([])
  const [notificationCount, setNotificationCount] = useState(0)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  useEffect(() => {
    fetchNotifications()
    // Fetch notifications every 30 seconds
    const interval = setInterval(fetchNotifications, 30000)
    return () => clearInterval(interval)
  }, [])

  const fetchNotifications = async () => {
    try {
      // Fetch notification count
      const countResponse = await fetch("/api/notifications/count")
      if (countResponse.ok) {
        const countData = await countResponse.json()
        setNotificationCount(countData.count || 0)
      }

      // Fetch actual notifications
      const notificationsResponse = await fetch("/api/notifications")
      if (notificationsResponse.ok) {
        const notificationsData = await notificationsResponse.json()
        setNotifications(notificationsData.notifications || [])
      }
    } catch (error) {
      console.error("Error fetching notifications:", error)
    }
  }

  const menuItems = [
    { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard', badge: 1 },
    { path: '/tracking-links', icon: Link2, label: 'Tracking Links', badge: 2 },
    { path: '/live-activity', icon: Activity, label: 'Live Activity', badge: 3 },
    { path: '/campaign', icon: Target, label: 'Campaign', badge: 4 },
    { path: '/analytics', icon: BarChart3, label: 'Analytics', badge: 5 },
    { path: '/geography', icon: Globe, label: 'Geography', badge: 6 },
    { path: '/security', icon: Shield, label: 'Security', badge: 7 },
    { path: '/settings', icon: Settings, label: 'Settings', badge: 8 },
    { path: '/link-shortener', icon: Scissors, label: 'Link Shortener', badge: 9 },
    { path: '/notifications', icon: Bell, label: 'Notifications', badge: 11, notificationCount: true },
    { path: '/admin-panel', icon: User, label: 'Admin Panel', badge: 10, adminOnly: true },
  ]

  const isActive = (path) => location.pathname === path

  return (
    <div className="flex h-screen bg-slate-900">
      {/* Mobile Menu Overlay */}
      {mobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Desktop Sidebar - Always visible on desktop */}
      <div className="hidden lg:flex w-64 bg-slate-800 border-r border-slate-700 flex-col">
        {/* Logo */}
        <div className="p-6 border-b border-slate-700">
          <Logo size="md" />
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          {menuItems.map((item) => {
            if (item.adminOnly && (!user || (user.role !== "admin" && user.role !== "main_admin"))) {
              return null
            }

            const Icon = item.icon
            return (
              <Button
                key={item.path}
                variant={isActive(item.path) ? "secondary" : "ghost"}
                className={`w-full justify-start text-left h-10 ${
                  isActive(item.path) 
                    ? 'bg-blue-600 text-white hover:bg-blue-700' 
                    : 'text-slate-300 hover:text-white hover:bg-slate-700'
                }`}
                onClick={() => navigate(item.path)}
              >
                <Icon className="mr-3 h-4 w-4" />
                {item.label}
                {item.badge && (
                  <Badge 
                    variant="secondary" 
                    className="ml-auto bg-slate-600 text-slate-200 text-xs"
                  >
                    {item.badge}
                  </Badge>
                )}
                {item.notificationCount && notificationCount > 0 && (
                  <Badge 
                    variant="destructive" 
                    className="ml-auto text-xs"
                  >
                    {notificationCount}
                  </Badge>
                )}
              </Button>
            )
          })}
        </nav>
      </div>

      {/* Mobile Sidebar */}
      <div className={`
        lg:hidden fixed inset-y-0 left-0 z-50 w-64 bg-slate-800 border-r border-slate-700 flex flex-col
        transform transition-transform duration-200 ease-in-out
        ${mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        {/* Logo & Mobile Close Button */}
        <div className="p-6 border-b border-slate-700 flex items-center justify-between">
          <Logo size="md" />
          <button
            onClick={() => setMobileMenuOpen(false)}
            className="text-slate-400 hover:text-white"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          {menuItems.map((item) => {
            if (item.adminOnly && (!user || (user.role !== "admin" && user.role !== "main_admin"))) {
              return null;
            }
            const Icon = item.icon
            const active = isActive(item.path)

            return (
              <button
                key={item.path}
                onClick={() => {
                  navigate(item.path)
                  setMobileMenuOpen(false)
                }}
                className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left transition-colors ${
                  active
                    ? 'bg-blue-600 text-white'
                    : 'text-slate-300 hover:bg-slate-700 hover:text-white'
                }`}
              >
                <Icon className="h-5 w-5" />
                <span className="flex-1">{item.label}</span>
                <Badge
                  variant={active ? "secondary" : "outline"}
                  className={`text-xs ${
                    active
                      ? 'bg-white text-blue-600'
                      : 'border-slate-600 text-slate-400'
                  }`}
                >
                  {item.notificationCount && notificationCount > 0 ? notificationCount : item.badge}
                </Badge>
              </button>
            )
          })}
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col lg:ml-0">
        {/* Mobile Header */}
        <header className="lg:hidden bg-slate-800 border-b border-slate-700 px-4 py-3 flex items-center justify-between">
          <button
            onClick={() => setMobileMenuOpen(true)}
            className="text-slate-400 hover:text-white p-2 rounded-md hover:bg-slate-700 transition-colors"
          >
            <Menu className="h-6 w-6" />
          </button>
          
          <Logo size="sm" />
          
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="border-blue-500 text-blue-400 bg-slate-700 text-xs px-2 py-1">
              {user?.role === 'main_admin' ? 'Main Admin' :
               user?.role === 'admin' ? 'Admin' : 'Member'}
            </Badge>
            {user && (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="text-slate-400 hover:text-white p-2 rounded-md hover:bg-slate-700">
                    <Avatar className="h-7 w-7">
                      <AvatarFallback className="bg-blue-600 text-white text-xs">
                        {user.email?.charAt(0).toUpperCase() || 'A'}
                      </AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="bg-slate-800 border-slate-700 w-48">
                  <DropdownMenuItem onClick={onLogout} className="text-slate-300 hover:text-white hover:bg-slate-700 cursor-pointer">
                    <LogOut className="mr-2 h-4 w-4" />
                    Logout
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            )}
          </div>
        </header>

        {/* Desktop Header */}
        <header className="hidden lg:flex bg-slate-800 border-b border-slate-700 px-6 py-4 items-center justify-between">
          <div className="flex items-center gap-4">
            <Badge variant="outline" className="border-blue-500 text-blue-400 bg-slate-700">
              <User className="h-3 w-3 mr-1" />
              A1
            </Badge>
            {user && (
              <Badge
                variant="outline"
                className={`text-xs ${
                  user.role === 'main_admin'
                    ? 'border-purple-500 text-purple-400 bg-purple-900/20'
                    : user.role === 'admin'
                    ? 'border-blue-500 text-blue-400 bg-blue-900/20'
                    : 'border-gray-500 text-gray-400 bg-gray-900/20'
                }`}
              >
                {user.role === 'main_admin' ? 'Main Admin' :
                 user.role === 'admin' ? 'Admin' : 'Member'}
              </Badge>
            )}
          </div>

          <div className="flex items-center gap-4">
            {/* Notifications */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <div className="relative">
                  <Button variant="ghost" size="sm" className="text-slate-400 hover:text-white">
                    <Bell className="h-5 w-5" />
                  </Button>
                  {notificationCount > 0 && (
                    <Badge className="absolute -top-2 -right-2 bg-red-500 text-white text-xs min-w-[20px] h-5 flex items-center justify-center rounded-full">
                      {notificationCount}
                    </Badge>
                  )}
                </div>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="bg-slate-800 border-slate-700 w-80">
                <div className="p-4">
                  <h3 className="text-white font-semibold mb-3">Notifications</h3>
                  <div className="space-y-3">
                    {notifications.length > 0 ? (
                      notifications.slice(0, 3).map((notification, index) => (
                        <div key={notification.id || index} className="p-3 bg-slate-700 rounded-lg">
                          <p className="text-slate-300 text-sm">{notification.message}</p>
                          <p className="text-slate-500 text-xs mt-1">{notification.timestamp}</p>
                        </div>
                      ))
                    ) : (
                      <p className="text-slate-400 text-sm">No new notifications</p>
                    )}
                  </div>
                </div>
              </DropdownMenuContent>
            </DropdownMenu>

            {/* User Menu */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="flex items-center gap-2 text-slate-400 hover:text-white">
                  <Avatar className="h-8 w-8 bg-blue-600">
                    <AvatarFallback className="bg-blue-600 text-white text-sm">
                      A
                    </AvatarFallback>
                  </Avatar>
                  <span className="text-sm hidden md:inline">admin@brainlinktracker.com</span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="bg-slate-800 border-slate-700">
                <DropdownMenuItem 
                  onClick={onLogout}
                  className="text-slate-300 hover:text-white hover:bg-slate-700 cursor-pointer"
                >
                  <LogOut className="h-4 w-4 mr-2" />
                  Sign Out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto bg-slate-900 p-4 lg:p-6">
          {children}
        </main>
      </div>
    </div>
  )
}

export default Layout
