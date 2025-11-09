import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Layout from './components/Layout'
import Dashboard from './components/Dashboard'
import Analytics from './components/Analytics'
import Campaign from './components/Campaign'
import Settings from './components/Settings'
import AdminPanel from './components/AdminPanel'
import LoginPage from './components/LoginPage'
import TrackingLinks from './components/TrackingLinks'
import Notifications from './components/Notifications'
import { toast } from 'sonner'

// Mock Auth Context/Hook
const useAuth = () => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate checking for token and fetching user data
    const token = localStorage.getItem('token')
    if (token) {
      // In a real app, you would verify the token with a backend call
      // For now, we'll mock a logged-in user
      setUser({ 
        id: 1, 
        username: 'Brain', 
        role: 'main_admin', 
        plan_type: 'enterprise' 
      })
    }
    setLoading(false)
  }, [])

  const login = async (username, password) => {
    // Simulate API call for login
    if (username === 'Brain' && password === 'Mayflower1!!') {
      const token = 'mock-jwt-token-main-admin'
      localStorage.setItem('token', token)
      setUser({ 
        id: 1, 
        username: 'Brain', 
        role: 'main_admin', 
        plan_type: 'enterprise' 
      })
      toast.success('Login successful!')
      return true
    } else if (username === '7thbrain' && password === 'Mayflower1!') {
      const token = 'mock-jwt-token-admin'
      localStorage.setItem('token', token)
      setUser({ 
        id: 2, 
        username: '7thbrain', 
        role: 'admin', 
        plan_type: 'pro' 
      })
      toast.success('Login successful!')
      return true
    } else {
      toast.error('Invalid credentials')
      return false
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
    toast.info('Logged out')
  }

  return { user, loading, login, logout }
}

// Protected Route Component
const ProtectedRoute = ({ children, allowedRoles }) => {
  const { user, loading } = useAuth()

  if (loading) {
    return <div>Loading...</div> // Or a proper spinner
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    toast.error('Access Denied: You do not have permission to view this page.')
    return <Navigate to="/dashboard" replace />
  }

  return children
}

const App = () => {
  const { user, loading, login, logout } = useAuth()

  if (loading) {
    return <div>Loading Application...</div>
  }

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage login={login} />} />
        
        <Route 
          path="/" 
          element={
            <ProtectedRoute>
              <Layout user={user} logout={logout} />
            </ProtectedRoute>
          }
        >
          <Route index element={<Dashboard />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="links" element={<TrackingLinks />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="campaigns" element={<Campaign />} />
          <Route path="settings" element={<Settings />} />
          <Route path="notifications" element={<Notifications />} />
          
          {/* Admin Protected Routes */}
          <Route 
            path="admin" 
            element={
              <ProtectedRoute allowedRoles={['main_admin', 'admin']}>
                <AdminPanel />
              </ProtectedRoute>
            } 
          />
          
          {/* Fallback for unknown routes */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
