import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Check, CreditCard, Loader2 } from 'lucide-react'
import { useToast } from '@/components/ui/use-toast'

const StripePaymentForm = () => {
  const [loading, setLoading] = useState(false)
  const [selectedPlan, setSelectedPlan] = useState(null)
  const { toast } = useToast()

  const plans = [
    {
      id: 'pro',
      name: 'Pro Plan',
      price: '$29.99',
      interval: '/month',
      features: [
        'Unlimited tracking links',
        'Advanced analytics',
        'Custom domains',
        'Priority support',
        'API access'
      ]
    },
    {
      id: 'enterprise',
      name: 'Enterprise Plan',
      price: '$99.99',
      interval: '/month',
      features: [
        'Everything in Pro',
        'Dedicated account manager',
        'Custom integrations',
        'SLA guarantee',
        'Advanced security features',
        'White-label solution'
      ]
    }
  ]

  const handleCheckout = async (planType) => {
    try {
      setLoading(true)
      setSelectedPlan(planType)

      // Get Stripe configuration
      const configResponse = await fetch('/api/payments/stripe/config')
      const config = await configResponse.json()

      if (!config.success) {
        throw new Error('Stripe is not configured')
      }

      // Create checkout session
      const response = await fetch('/api/payments/stripe/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          plan_type: planType
        })
      })

      const data = await response.json()

      if (data.success && data.sessionId) {
        // Load Stripe and redirect to checkout
        const stripe = await window.Stripe(config.publishableKey)
        const { error } = await stripe.redirectToCheckout({
          sessionId: data.sessionId
        })

        if (error) {
          throw new Error(error.message)
        }
      } else {
        throw new Error(data.error || 'Failed to create checkout session')
      }
    } catch (error) {
      console.error('Checkout error:', error)
      toast({
        title: 'Error',
        description: error.message || 'Failed to process payment',
        variant: 'destructive'
      })
    } finally {
      setLoading(false)
      setSelectedPlan(null)
    }
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {plans.map((plan) => (
          <Card key={plan.id} className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center justify-between">
                {plan.name}
                {plan.id === 'enterprise' && (
                  <Badge className="bg-blue-600 text-white">Popular</Badge>
                )}
              </CardTitle>
              <CardDescription>
                <span className="text-3xl font-bold text-white">{plan.price}</span>
                <span className="text-slate-400">{plan.interval}</span>
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3 mb-6">
                {plan.features.map((feature, index) => (
                  <li key={index} className="flex items-start gap-2 text-slate-300">
                    <Check className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>

              <Button
                onClick={() => handleCheckout(plan.id)}
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white"
              >
                {loading && selectedPlan === plan.id ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <CreditCard className="mr-2 h-4 w-4" />
                    Subscribe Now
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="bg-slate-800 border-slate-700">
        <CardContent className="pt-6">
          <div className="flex items-center gap-2 text-slate-400 text-sm">
            <Check className="h-4 w-4 text-green-500" />
            <span>Secure payment processing by Stripe</span>
          </div>
          <div className="flex items-center gap-2 text-slate-400 text-sm mt-2">
            <Check className="h-4 w-4 text-green-500" />
            <span>Cancel anytime - no questions asked</span>
          </div>
        </CardContent>
      </Card>

      {/* Load Stripe.js */}
      <script src="https://js.stripe.com/v3/"></script>
    </div>
  )
}

export default StripePaymentForm
