
import { formatDistanceToNow } from 'date-fns'

export const formatNotificationTime = (timestamp) => {
  try {
    const date = new Date(timestamp)
    const now = new Date()
    const diffInMinutes = Math.floor((now - date) / (1000 * 60))
    
    if (diffInMinutes < 1) return 'Just now'
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`
    
    return formatDistanceToNow(date, { addSuffix: true })
  } catch (error) {
    return 'Unknown time'
  }
}

export const useRealTimeNotifications = () => {
  const [notifications, setNotifications] = useState([])
  const [lastUpdate, setLastUpdate] = useState(Date.now())
  
  useEffect(() => {
    const interval = setInterval(() => {
      setLastUpdate(Date.now())
    }, 30000) // Update every 30 seconds
    
    return () => clearInterval(interval)
  }, [])
  
  const fetchNotifications = async () => {
    try {
      const response = await fetch('/api/notifications', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setNotifications(data.notifications || [])
      }
    } catch (error) {
      console.error('Error fetching notifications:', error)
    }
  }
  
  useEffect(() => {
    fetchNotifications()
    
    // Set up real-time updates
    const interval = setInterval(fetchNotifications, 60000) // Every minute
    return () => clearInterval(interval)
  }, [])
  
  return { notifications, lastUpdate, refresh: fetchNotifications }
}
