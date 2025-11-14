import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { 
  Link2, BarChart3, Shield, Zap, Globe, TrendingUp, 
  Users, Lock, Smartphone, Code, Bell, FileText,
  ArrowRight, Check
} from 'lucide-react'
import { motion } from 'framer-motion'
import Logo from './Logo'

const FeaturesPage = () => {
  const navigate = useNavigate()

  const features = [
    {
      icon: <Link2 className="w-10 h-10 text-blue-400" />,
      title: 'Smart Link Shortening',
      description: 'Create short, branded links that are easy to share and remember. Customize your links with your own domain for better brand recognition.',
      benefits: ['Custom domains', 'Bulk link creation', 'QR code generation', 'Link expiration']
    },
    {
      icon: <BarChart3 className="w-10 h-10 text-purple-400" />,
      title: 'Advanced Analytics',
      description: 'Get comprehensive insights into your link performance with real-time analytics and detailed reports.',
      benefits: ['Real-time tracking', 'Geographic data', 'Device analytics', 'Referrer tracking']
    },
    {
      icon: <Shield className="w-10 h-10 text-green-400" />,
      title: 'Enterprise Security',
      description: 'Bank-level encryption and advanced security features to protect your data and ensure compliance.',
      benefits: ['SSL encryption', '2FA authentication', 'Role-based access', 'Audit logs']
    },
    {
      icon: <Zap className="w-10 h-10 text-yellow-400" />,
      title: 'Lightning Fast',
      description: 'Optimized infrastructure ensures your links redirect instantly with 99.9% uptime guarantee.',
      benefits: ['Global CDN', 'Sub-second redirects', 'Auto-scaling', 'DDoS protection']
    },
    {
      icon: <TrendingUp className="w-10 h-10 text-pink-400" />,
      title: 'Campaign Management',
      description: 'Organize and track marketing campaigns with custom tags, UTM parameters, and conversion tracking.',
      benefits: ['UTM builder', 'Campaign grouping', 'A/B testing', 'Conversion tracking']
    },
    {
      icon: <Users className="w-10 h-10 text-cyan-400" />,
      title: 'Team Collaboration',
      description: 'Work together seamlessly with team workspaces, shared links, and role-based permissions.',
      benefits: ['Team workspaces', 'Shared folders', 'Permission controls', 'Activity feed']
    },
    {
      icon: <Code className="w-10 h-10 text-indigo-400" />,
      title: 'Developer API',
      description: 'Powerful REST API with comprehensive documentation for seamless integration into your applications.',
      benefits: ['RESTful API', 'Webhooks', 'SDKs available', 'API documentation']
    },
    {
      icon: <Bell className="w-10 h-10 text-orange-400" />,
      title: 'Smart Notifications',
      description: 'Stay informed with real-time notifications about link performance, security alerts, and team activity.',
      benefits: ['Email alerts', 'Slack integration', 'Custom triggers', 'Daily reports']
    },
    {
      icon: <Smartphone className="w-10 h-10 text-teal-400" />,
      title: 'Mobile Optimized',
      description: 'Fully responsive design works perfectly on all devices, with dedicated mobile apps coming soon.',
      benefits: ['Responsive design', 'Touch-friendly', 'Mobile analytics', 'PWA support']
    },
    {
      icon: <Lock className="w-10 h-10 text-red-400" />,
      title: 'Password Protection',
      description: 'Add an extra layer of security with password-protected links and access controls.',
      benefits: ['Link passwords', 'Expiration dates', 'Click limits', 'IP restrictions']
    },
    {
      icon: <Globe className="w-10 h-10 text-emerald-400" />,
      title: 'Geographic Targeting',
      description: 'Route users to different destinations based on their location for personalized experiences.',
      benefits: ['Country targeting', 'City-level routing', 'Language detection', 'Custom rules']
    },
    {
      icon: <FileText className="w-10 h-10 text-violet-400" />,
      title: 'Detailed Reports',
      description: 'Generate comprehensive reports with customizable metrics and export options for data analysis.',
      benefits: ['Custom reports', 'CSV export', 'Scheduled reports', 'White-label PDFs']
    }
  ]

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
              <Button variant="ghost" onClick={() => navigate('/pricing')} className="text-slate-300 hover:text-white">
                Pricing
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
              Powerful Features for
              <br />
              <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Modern Link Management
              </span>
            </h1>
            <p className="text-xl text-slate-400 max-w-3xl mx-auto mb-8">
              Everything you need to create, track, and optimize your links. From basic shortening to advanced analytics and team collaboration.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.05 }}
              >
                <Card className="bg-slate-800/50 border-slate-700 hover:border-slate-600 transition-all h-full">
                  <CardHeader>
                    <div className="mb-4">{feature.icon}</div>
                    <CardTitle className="text-white text-xl mb-2">{feature.title}</CardTitle>
                    <CardDescription className="text-slate-400">
                      {feature.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {feature.benefits.map((benefit, idx) => (
                        <li key={idx} className="flex items-center text-sm text-slate-300">
                          <Check className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
                          {benefit}
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
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
              Ready to Experience These Features?
            </h2>
            <p className="text-lg text-slate-400 mb-8">
              Start your free trial today and see how Brain Link Tracker can transform your link management.
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
                onClick={() => navigate('/pricing')}
                className="border-slate-700 text-white hover:bg-slate-800 text-lg px-8 py-6"
              >
                View Pricing
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
              <Logo size="md" />
              <p className="text-slate-400 text-sm mt-4">
                The most powerful link management platform for modern businesses.
              </p>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-slate-400 text-sm">
                <li><button onClick={() => navigate('/features')} className="hover:text-white transition-colors">Features</button></li>
                <li><button onClick={() => navigate('/pricing')} className="hover:text-white transition-colors">Pricing</button></li>
                <li><button onClick={() => navigate('/contact')} className="hover:text-white transition-colors">Contact</button></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-slate-400 text-sm">
                <li><button onClick={() => navigate('/contact')} className="hover:text-white transition-colors">About Us</button></li>
                <li><button onClick={() => navigate('/contact')} className="hover:text-white transition-colors">Contact</button></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Legal</h3>
              <ul className="space-y-2 text-slate-400 text-sm">
                <li><button className="hover:text-white transition-colors">Privacy Policy</button></li>
                <li><button className="hover:text-white transition-colors">Terms of Service</button></li>
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

export default FeaturesPage