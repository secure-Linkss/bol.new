import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Check, ArrowRight, Zap, Shield, TrendingUp, Users } from 'lucide-react'
import { motion } from 'framer-motion'
import Logo from './Logo'

const PricingPage = () => {
  const navigate = useNavigate()
  const [billingCycle, setBillingCycle] = useState('monthly')

  const plans = [
    {
      name: 'Free Trial',
      price: '$0',
      period: '7 days',
      description: 'Perfect for trying out our platform',
      features: [
        '10 links per day',
        'Basic analytics',
        'Email support',
        '7-day trial period',
        'No credit card required'
      ],
      cta: 'Start Free Trial',
      popular: false,
      planType: 'free'
    },
    {
      name: 'Weekly',
      price: '$35',
      period: '7 days',
      description: 'Great for short-term campaigns',
      features: [
        'Unlimited links',
        'Advanced analytics',
        'Priority support',
        'Custom domains',
        'API access'
      ],
      cta: 'Get Started',
      popular: false,
      planType: 'weekly'
    },
    {
      name: 'Biweekly',
      price: '$68',
      period: '14 days',
      description: 'Best value for bi-weekly needs',
      features: [
        'Everything in Weekly',
        'A/B testing',
        'Team collaboration',
        'Advanced reporting',
        'Dedicated support'
      ],
      cta: 'Get Started',
      popular: true,
      planType: 'biweekly'
    },
    {
      name: 'Monthly',
      price: '$150',
      period: '30 days',
      description: 'Most popular for businesses',
      features: [
        'Everything in Biweekly',
        'White-label options',
        'Custom integrations',
        'Priority API access',
        '24/7 phone support'
      ],
      cta: 'Get Started',
      popular: false,
      planType: 'monthly'
    },
    {
      name: 'Quarterly',
      price: '$420',
      period: '90 days',
      description: 'Save 7% with quarterly billing',
      features: [
        'Everything in Monthly',
        'Quarterly business reviews',
        'Custom training',
        'Advanced security',
        'SLA guarantee'
      ],
      cta: 'Get Started',
      popular: false,
      planType: 'quarterly'
    },
    {
      name: 'Pro',
      price: '$299',
      period: 'per month',
      description: 'For growing teams',
      features: [
        'Unlimited everything',
        'Advanced team features',
        'Custom branding',
        'API rate limit increase',
        'Dedicated account manager'
      ],
      cta: 'Get Started',
      popular: false,
      planType: 'pro'
    },
    {
      name: 'Enterprise',
      price: '$999',
      period: 'per year',
      description: 'For large organizations',
      features: [
        'Everything in Pro',
        'Custom contracts',
        'On-premise deployment',
        'Unlimited team members',
        'Enterprise SLA'
      ],
      cta: 'Contact Sales',
      popular: false,
      planType: 'enterprise'
    }
  ]

  const handleSelectPlan = (planType) => {
    navigate(`/register?plan=${planType}`)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-950/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="cursor-pointer" onClick={() => navigate('/')}>
              <Logo size="md" />
            </div>
            <div className="flex items-center gap-4">
              <Button variant="ghost" onClick={() => navigate('/')} className="text-slate-300 hover:text-white">
                Home
              </Button>
              <Button variant="ghost" onClick={() => navigate('/features')} className="text-slate-300 hover:text-white">
                Features
              </Button>
              <Button variant="ghost" onClick={() => navigate('/contact')} className="text-slate-300 hover:text-white">
                Contact
              </Button>
              <Button onClick={() => navigate('/login')} className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white">
                Sign In
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6">
              Simple, Transparent Pricing
            </h1>
            <p className="text-xl text-slate-400 max-w-3xl mx-auto mb-8">
              Choose the perfect plan for your needs. All plans include our core features with no hidden fees.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
            {plans.map((plan, index) => (
              <motion.div
                key={plan.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <Card className={`relative h-full flex flex-col ${
                  plan.popular 
                    ? 'bg-gradient-to-b from-blue-900/20 to-purple-900/20 border-blue-500' 
                    : 'bg-slate-900 border-slate-800'
                }`}>
                  {plan.popular && (
                    <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                      <span className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                        Most Popular
                      </span>
                    </div>
                  )}
                  <CardHeader>
                    <CardTitle className="text-2xl font-bold text-white">{plan.name}</CardTitle>
                    <CardDescription className="text-slate-400">{plan.description}</CardDescription>
                    <div className="mt-4">
                      <span className="text-4xl font-bold text-white">{plan.price}</span>
                      <span className="text-slate-400 ml-2">/ {plan.period}</span>
                    </div>
                  </CardHeader>
                  <CardContent className="flex-1 flex flex-col">
                    <ul className="space-y-3 mb-6 flex-1">
                      {plan.features.map((feature, idx) => (
                        <li key={idx} className="flex items-start">
                          <Check className="w-5 h-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                          <span className="text-slate-300">{feature}</span>
                        </li>
                      ))}
                    </ul>
                    <Button
                      onClick={() => handleSelectPlan(plan.planType)}
                      className={`w-full ${
                        plan.popular
                          ? 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white'
                          : 'bg-slate-800 hover:bg-slate-700 text-white'
                      }`}
                    >
                      {plan.cta}
                      <ArrowRight className="ml-2 w-4 h-4" />
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Comparison */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-900/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-white text-center mb-12">
            Why Choose Brain Link Tracker?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <Zap className="w-10 h-10 text-blue-400 mb-2" />
                <CardTitle className="text-white">Lightning Fast</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-slate-400">
                  Track and analyze your links in real-time with our high-performance infrastructure.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <Shield className="w-10 h-10 text-purple-400 mb-2" />
                <CardTitle className="text-white">Secure & Private</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-slate-400">
                  Enterprise-grade security with end-to-end encryption and GDPR compliance.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <TrendingUp className="w-10 h-10 text-green-400 mb-2" />
                <CardTitle className="text-white">Advanced Analytics</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-slate-400">
                  Get deep insights with our powerful analytics and reporting tools.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <Users className="w-10 h-10 text-pink-400 mb-2" />
                <CardTitle className="text-white">Team Collaboration</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-slate-400">
                  Work together seamlessly with team features and role-based access.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-white text-center mb-12">
            Frequently Asked Questions
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white text-lg">Can I change plans later?</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-slate-400">
                  Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white text-lg">What payment methods do you accept?</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-slate-400">
                  We accept all major credit cards, PayPal, and cryptocurrency payments for your convenience.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white text-lg">Is there a free trial?</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-slate-400">
                  Yes! All new users get a 7-day free trial with 10 links per day. No credit card required to start.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white text-lg">What happens when my plan expires?</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-slate-400">
                  Your account will be downgraded to the free plan. Your data is preserved, but you'll be limited to 10 links per day until you renew.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-blue-900/30 to-purple-900/30">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-6">
              Ready to Get Started?
            </h2>
            <p className="text-lg text-slate-400 mb-8">
              Join thousands of businesses already using Brain Link Tracker. Start your free trial today.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg"
                onClick={() => navigate('/register')}
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white text-lg px-8 py-6"
              >
                Start Free Trial
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
              <Button 
                size="lg"
                variant="outline"
                onClick={() => navigate('/contact')}
                className="border-slate-700 text-white hover:bg-slate-800 text-lg px-8 py-6"
              >
                Contact Sales
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-950 border-t border-slate-800 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="mb-4">
                <Logo size="md" />
              </div>
              <p className="text-slate-400 text-sm">
                The most powerful link management platform for modern businesses.
              </p>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-slate-400 text-sm">
                <li><Link to="/features" className="hover:text-white transition-colors">Features</Link></li>
                <li><Link to="/pricing" className="hover:text-white transition-colors">Pricing</Link></li>
                <li><Link to="/contact" className="hover:text-white transition-colors">Contact</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-slate-400 text-sm">
                <li><Link to="/about" className="hover:text-white transition-colors">About Us</Link></li>
                <li><Link to="/contact" className="hover:text-white transition-colors">Contact</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Legal</h3>
              <ul className="space-y-2 text-slate-400 text-sm">
                <li><Link to="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link></li>
                <li><Link to="/terms" className="hover:text-white transition-colors">Terms of Service</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-slate-800 pt-8 text-center text-slate-400 text-sm">
            <p>&copy; {new Date().getFullYear()} Brain Link Tracker. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default PricingPage