
// Metrics calculation fix for accurate visitor vs clicks tracking
export const calculateAccurateMetrics = async (linkId) => {
  try {
    const response = await fetch(`/api/links/${linkId}/metrics`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      return {
        totalClicks: data.total_clicks || 0,
        uniqueVisitors: data.unique_visitors || 0, 
        conversionRate: data.conversion_rate || 0,
        clickToVisitorRatio: data.unique_visitors > 0 ? (data.total_clicks / data.unique_visitors * 100).toFixed(1) : 0
      };
    }
  } catch (error) {
    console.error('Error calculating metrics:', error);
    return { totalClicks: 0, uniqueVisitors: 0, conversionRate: 0, clickToVisitorRatio: 0 };
  }
};

// Real-time notification timestamp formatting
export const formatNotificationTime = (timestamp) => {
  const now = new Date();
  const notificationTime = new Date(timestamp);
  const diffInMinutes = Math.floor((now - notificationTime) / (1000 * 60));
  
  if (diffInMinutes < 1) return 'Now';
  if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
  if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
  return `${Math.floor(diffInMinutes / 1440)}d ago`;
};
