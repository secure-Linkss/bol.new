import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Label } from './ui/label'
import { Copy, Wallet, Loader, CheckCircle, AlertCircle } from 'lucide-react'
import { toast } from 'sonner'
import { Alert, AlertDescription } from './ui/alert'

const CryptoPaymentForm = ({ planType, planPrice, onSuccess, onCancel }) => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [walletAddresses, setWalletAddresses] = useState(null)
  const [paymentDetails, setPaymentDetails] = useState({
    cryptoType: 'bitcoin',
    amount: planPrice || 0,
    screenshot: null
  })
  const [verificationId, setVerificationId] = useState(null)
  const [isVerificationPending, setIsVerificationPending] = useState(false)

  // Updated plan names mapping
  const planNames = {
    'weekly': 'Weekly',
    'biweekly': 'Biweekly',
    'monthly': 'Monthly',
    'quarterly': 'Quarterly'
  }

  useEffect(() => {
    fetchWalletAddresses()
  }, [])

  const fetchWalletAddresses = async () => {
    try {
      const response = await fetch('/api/admin/system-config', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (!response.ok) throw new Error('Failed to fetch wallet addresses')
      const data = await response.json()
      setWalletAddresses({
        bitcoin: data.crypto_bitcoin_address,
        ethereum: data.crypto_ethereum_address
      })
    } catch (e) {
      setError(e.message)
      toast.error(e.message)
    }
  }

  const initiatePayment = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('/api/payments/subscribe/crypto', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          plan_type: planType,
          crypto_type: paymentDetails.cryptoType,
          amount: paymentDetails.amount
        })
      })

      const data = await response.json()

      if (!response.ok) throw new Error(data.msg || 'Failed to initiate crypto payment')

      setVerificationId(data.verification_id)
      setIsVerificationPending(true)
      toast.success('Payment initiated. Please transfer the funds.')

    } catch (e) {
      setError(e.message)
      toast.error(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleScreenshotUpload = (e) => {
    setPaymentDetails(prev => ({ ...prev, screenshot: e.target.files[0] }))
  }

  const submitVerification = async () => {
    if (!paymentDetails.screenshot) {
      setError('Please upload a screenshot of the transaction.')
      return
    }

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('verification_id', verificationId)
    formData.append('screenshot', paymentDetails.screenshot)

    try {
      const response = await fetch('/api/payments/crypto/verify', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: formData
      })

      const data = await response.json()

      if (!response.ok) throw new Error(data.msg || 'Failed to submit verification')

      toast.success(data.msg)
      onSuccess()

    } catch (e) {
      setError(e.message)
      toast.error(e.message)
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    toast.info('Address copied to clipboard!')
  }

  const currentAddress = walletAddresses ? walletAddresses[paymentDetails.cryptoType] : 'Loading...'

  return (
    <Card className="bg-slate-700 border-slate-600">
      <CardHeader>
        <CardTitle className="text-white flex items-center gap-2">
          <Wallet className="h-5 w-5 text-orange-400" /> Crypto Payment for {planNames[planType]} Plan
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {error && (
          <Alert variant="destructive" className="bg-red-900/20 border-red-700">
            <AlertCircle className="h-4 w-4 text-red-500" />
            <AlertDescription className="text-red-400">{error}</AlertDescription>
          </Alert>
        )}

        {!isVerificationPending ? (
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <Label htmlFor="crypto-bitcoin" className="flex items-center space-x-2 text-white">
                <Input
                  id="crypto-bitcoin"
                  type="radio"
                  name="crypto-type"
                  value="bitcoin"
                  checked={paymentDetails.cryptoType === 'bitcoin'}
                  onChange={() => setPaymentDetails(prev => ({ ...prev, cryptoType: 'bitcoin' }))}
                  className="form-radio text-orange-600 bg-slate-600 border-slate-500"
                />
                <span>Bitcoin</span>
              </Label>
              <Label htmlFor="crypto-ethereum" className="flex items-center space-x-2 text-white">
                <Input
                  id="crypto-ethereum"
                  type="radio"
                  name="crypto-type"
                  value="ethereum"
                  checked={paymentDetails.cryptoType === 'ethereum'}
                  onChange={() => setPaymentDetails(prev => ({ ...prev, cryptoType: 'ethereum' }))}
                  className="form-radio text-orange-600 bg-slate-600 border-slate-500"
                />
                <span>Ethereum</span>
              </Label>
            </div>

            <div className="space-y-2">
              <Label className="text-slate-300">Amount to Pay</Label>
              <Input
                type="text"
                value={`$${paymentDetails.amount} USD`}
                readOnly
                className="bg-slate-600 border-slate-500 text-white font-bold"
              />
            </div>

            <Button onClick={initiatePayment} disabled={loading || !walletAddresses} className="w-full bg-orange-600 hover:bg-orange-700 text-white">
              {loading ? <Loader className="mr-2 h-4 w-4 animate-spin" /> : <Wallet className="mr-2 h-4 w-4" />}
              {loading ? 'Initiating...' : 'Initiate Crypto Payment'}
            </Button>
            <Button onClick={onCancel} variant="outline" className="w-full border-slate-500 text-slate-300 hover:bg-slate-600">
              Cancel
            </Button>
          </div>
        ) : (
          <div className="space-y-6">
            <Alert className="bg-orange-900/20 border-orange-700">
              <AlertCircle className="h-4 w-4 text-orange-500" />
              <AlertDescription className="text-orange-400">
                **Payment Pending.** Please transfer **${paymentDetails.amount} USD** worth of {paymentDetails.cryptoType.toUpperCase()} to the address below and upload a screenshot of the transaction.
              </AlertDescription>
            </Alert>

            <div className="space-y-2">
              <Label className="text-slate-300">{paymentDetails.cryptoType.toUpperCase()} Wallet Address</Label>
              <div className="flex items-center space-x-2">
                <Input
                  type="text"
                  value={currentAddress}
                  readOnly
                  className="bg-slate-600 border-slate-500 text-white"
                />
                <Button variant="outline" size="icon" onClick={() => copyToClipboard(currentAddress)} className="border-slate-500 text-slate-300 hover:bg-slate-600">
                  <Copy className="h-4 w-4" />
                </Button>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="screenshot" className="text-slate-300">Upload Transaction Screenshot</Label>
              <Input
                id="screenshot"
                type="file"
                accept="image/*"
                onChange={handleScreenshotUpload}
                className="bg-slate-600 border-slate-500 text-white file:text-white file:bg-blue-600 file:border-none hover:file:bg-blue-700"
              />
              {paymentDetails.screenshot && <p className="text-sm text-green-400">File selected: {paymentDetails.screenshot.name}</p>}
            </div>

            <Button onClick={submitVerification} disabled={loading || !paymentDetails.screenshot} className="w-full bg-green-600 hover:bg-green-700 text-white">
              {loading ? <Loader className="mr-2 h-4 w-4 animate-spin" /> : <CheckCircle className="mr-2 h-4 w-4" />}
              {loading ? 'Submitting...' : 'Submit for Verification'}
            </Button>
            <Button onClick={onCancel} variant="outline" className="w-full border-slate-500 text-slate-300 hover:bg-slate-600">
              Cancel
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default CryptoPaymentForm
