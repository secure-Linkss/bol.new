import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Label } from './ui/label'
import { CreditCard, Loader, CheckCircle, AlertCircle } from 'lucide-react'
import { toast } from 'sonner'
import { Alert, AlertDescription } from './ui/alert'

const StripePaymentForm = ({ planType, onSuccess, onCancel }) => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [formData, setFormData] = useState({
    cardNumber: '',
    expiryDate: '',
    cvc: '',
    cardholderName: ''
  })

  // Updated plan names mapping
  const planNames = {
    'weekly': 'Weekly',
    'biweekly': 'Biweekly',
    'monthly': 'Monthly',
    'quarterly': 'Quarterly'
  }

  const formatCardNumber = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '')
    const matches = v.match(/\d{4,16}/g)
    const match = (matches && matches[0]) || ''
    const parts = []
    for (let i = 0; i < match.length; i += 4) {
      parts.push(match.substring(i, i + 4))
    }
    return parts.length ? parts.join(' ') : value
  }

  const formatExpiryDate = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '')
    if (v.length > 2) {
      return `${v.substring(0, 2)} / ${v.substring(2, 4)}`
    }
    return v
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    let formattedValue = value

    if (name === 'cardNumber') {
      formattedValue = formatCardNumber(value)
    } else if (name === 'expiryDate') {
      formattedValue = formatExpiryDate(value)
    } else if (name === 'cvc') {
      formattedValue = value.replace(/[^0-9]/gi, '').substring(0, 4)
    }

    setFormData(prev => ({ ...prev, [name]: formattedValue }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      // Step 1: Create a Stripe Checkout Session on the backend
      const response = await fetch('/api/payments/subscribe/stripe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ plan_type: planType })
      })

      const data = await response.json()

      if (!response.ok) throw new Error(data.msg || 'Failed to initiate Stripe payment')

      // Step 2: Redirect to Stripe Checkout
      // In a real application, you would use Stripe.js to redirect
      // For this mock, we will simulate the redirect and success
      toast.info('Redirecting to Stripe Checkout...')
      
      // Simulate successful payment flow
      setTimeout(() => {
        toast.success('Stripe Checkout initiated successfully. Assuming payment success for demo.')
        onSuccess()
      }, 2000)

    } catch (e) {
      setError(e.message)
      toast.error(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="bg-slate-700 border-slate-600">
      <CardHeader>
        <CardTitle className="text-white flex items-center gap-2">
          <CreditCard className="h-5 w-5 text-blue-400" /> Card Payment for {planNames[planType]} Plan
        </CardTitle>
      </CardHeader>
      <CardContent>
        {error && (
          <Alert variant="destructive" className="bg-red-900/20 border-red-700 mb-4">
            <AlertCircle className="h-4 w-4 text-red-500" />
            <AlertDescription className="text-red-400">{error}</AlertDescription>
          </Alert>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="cardholderName" className="text-slate-300">Cardholder Name</Label>
            <Input
              id="cardholderName"
              name="cardholderName"
              type="text"
              placeholder="Jane Doe"
              value={formData.cardholderName}
              onChange={handleChange}
              required
              className="bg-slate-600 border-slate-500 text-white"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="cardNumber" className="text-slate-300">Card Number</Label>
            <Input
              id="cardNumber"
              name="cardNumber"
              type="text"
              placeholder="XXXX XXXX XXXX XXXX"
              value={formData.cardNumber}
              onChange={handleChange}
              maxLength="19"
              required
              className="bg-slate-600 border-slate-500 text-white"
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="expiryDate" className="text-slate-300">Expiry Date (MM / YY)</Label>
              <Input
                id="expiryDate"
                name="expiryDate"
                type="text"
                placeholder="MM / YY"
                value={formData.expiryDate}
                onChange={handleChange}
                maxLength="7"
                required
                className="bg-slate-600 border-slate-500 text-white"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="cvc" className="text-slate-300">CVC</Label>
              <Input
                id="cvc"
                name="cvc"
                type="text"
                placeholder="CVC"
                value={formData.cvc}
                onChange={handleChange}
                maxLength="4"
                required
                className="bg-slate-600 border-slate-500 text-white"
              />
            </div>
          </div>
          <Button type="submit" disabled={loading} className="w-full bg-blue-600 hover:bg-blue-700 text-white">
            {loading ? <Loader className="mr-2 h-4 w-4 animate-spin" /> : <CheckCircle className="mr-2 h-4 w-4" />}
            {loading ? 'Processing...' : 'Pay and Subscribe'}
          </Button>
          <Button onClick={onCancel} variant="outline" className="w-full border-slate-500 text-slate-300 hover:bg-slate-600">
            Cancel
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}

export default StripePaymentForm
