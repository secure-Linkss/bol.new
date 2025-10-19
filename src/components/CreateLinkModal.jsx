import { useState, useEffect } from 'react'

const CreateLinkModal = ({ isOpen, onClose, onLinkCreated }) => {
  const [formData, setFormData] = useState({
    originalUrl: '',
    title: '',
    campaign: '',
    domain: 'vercel',
    customDomain: '',
    expiryDate: '',
    password: '',
    description: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [adminDomains, setAdminDomains] = useState([])
  const [domainsLoading, setDomainsLoading] = useState(true)

  // Fetch admin-loaded domains on component mount
  useEffect(() => {
    if (isOpen) {
      fetchAdminDomains()
    }
  }, [isOpen])

  const fetchAdminDomains = async () => {
    try {
      setDomainsLoading(true)
      const token = localStorage.getItem('token')
      const response = await fetch('/api/admin/domains', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        const domains = Array.isArray(data) ? data : data.items || []
        const activeDomains = domains.filter(d => d.is_active)
        setAdminDomains(activeDomains)
      }
    } catch (error) {
      console.error('Failed to fetch admin domains:', error)
      setAdminDomains([])
    } finally {
      setDomainsLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await fetch('/api/links/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        const data = await response.json()
        onLinkCreated(data.link)
        onClose()
        setFormData({
          originalUrl: '',
          title: '',
          campaign: '',
          domain: 'vercel',
          customDomain: '',
          expiryDate: '',
          password: '',
          description: ''
        })
      } else {
        const errorData = await response.json()
        setError(errorData.error || 'Failed to create link')
      }
    } catch (error) {
      setError('Network error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-900 rounded-lg p-6 w-full max-w-2xl mx-4 border border-gray-800 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-white">Create Short Link</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-300 text-2xl"
          >
            ✕
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-900 border border-red-600 text-red-200 rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Original URL */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Original URL <span className="text-red-500">*</span>
            </label>
            <input
              type="url"
              name="originalUrl"
              value={formData.originalUrl}
              onChange={handleChange}
              placeholder="https://example.com/your-long-url"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Title
            </label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="Link title (optional)"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Campaign */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Campaign
            </label>
            <input
              type="text"
              name="campaign"
              value={formData.campaign}
              onChange={handleChange}
              placeholder="Campaign name (optional)"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Domain Selection */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Domain <span className="text-red-500">*</span>
              </label>
              <select
                name="domain"
                value={formData.domain}
                onChange={handleChange}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="vercel">Vercel Domain (Default)</option>
                {domainsLoading ? (
                  <option disabled>Loading domains...</option>
                ) : adminDomains.length > 0 ? (
                  <>
                    <optgroup label="Admin-Loaded Domains">
                      {adminDomains.map(domain => (
                        <option key={domain.id} value={domain.domain}>
                          {domain.domain} {domain.description ? `- ${domain.description}` : ''}
                        </option>
                      ))}
                    </optgroup>
                  </>
                ) : null}
                <optgroup label="Other Options">
                  <option value="shortio">Short.io Integration</option>
                  <option value="custom">Custom Domain</option>
                </optgroup>
              </select>
              <p className="text-xs text-gray-400 mt-1">
                {adminDomains.length > 0 ? `${adminDomains.length} admin domains available` : 'No custom domains loaded yet'}
              </p>
            </div>

            {/* Custom Domain Input */}
            {(formData.domain === 'custom' || (formData.domain !== 'vercel' && formData.domain !== 'shortio' && !adminDomains.some(d => d.domain === formData.domain))) && (
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Custom Domain
                </label>
                <input
                  type="text"
                  name="customDomain"
                  value={formData.customDomain}
                  onChange={handleChange}
                  placeholder="yourdomain.com"
                  className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            )}
          </div>

          {/* Expiry Date */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Expiry Date (Optional)
            </label>
            <input
              type="date"
              name="expiryDate"
              value={formData.expiryDate}
              onChange={handleChange}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Password Protection */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Password Protection (Optional)
            </label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Password to access link"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Link description (optional)"
              rows="3"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4 border-t border-gray-700">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-700 text-gray-300 rounded-md hover:bg-gray-800 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
            >
              {loading ? 'Creating...' : 'Create Link'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CreateLinkModal

