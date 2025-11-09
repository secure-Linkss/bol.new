#!/bin/bash

echo "=========================================="
echo "DEPLOYING BRAIN LINK TRACKER TO VERCEL"
echo "=========================================="

# Install Vercel CLI
echo "Installing Vercel CLI..."
npm install -g vercel

# Set Vercel token
export VERCEL_TOKEN="2so8HRWfD06D8dBcs6D20mSx"

# Deploy to Vercel with environment variables
echo ""
echo "Deploying to Vercel with environment variables..."
echo ""

vercel --token="$VERCEL_TOKEN" \
  --name="secureaccountshub" \
  --prod \
  --yes \
  --env DATABASE_URL="postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" \
  --env SECRET_KEY="ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE" \
  --env SHORTIO_API_KEY="sk_DbGGlUHPN7Z9VotL" \
  --env SHORTIO_DOMAIN="Secure-links.short.gy" \
  --env STRIPE_SECRET_KEY="sk_test_your_test_key_here" \
  --env STRIPE_PUBLISHABLE_KEY="pk_test_your_test_key_here"

echo ""
echo "=========================================="
echo "DEPLOYMENT COMPLETE!"
echo "=========================================="
