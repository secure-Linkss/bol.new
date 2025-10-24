#!/bin/bash

echo "===================================="
echo "BRAIN LINK TRACKER - DEPLOYMENT"
echo "===================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "ERROR: Not a git repository"
    exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Detected changes, committing..."
    
    git add .
    
    echo "Enter commit message (or press Enter for default):"
    read commit_msg
    
    if [ -z "$commit_msg" ]; then
        commit_msg="Production deployment: Critical fixes and enhancements"
    fi
    
    git commit -m "$commit_msg"
    echo "✓ Changes committed"
else
    echo "✓ No uncommitted changes"
fi

# Push to GitHub
echo ""
echo "🚀 Pushing to GitHub..."
git push origin master

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "Next steps:"
    echo "1. Vercel will automatically deploy from GitHub"
    echo "2. Monitor deployment at: https://vercel.com/dashboard"
    echo "3. Check logs for any errors"
    echo "4. Test the deployment at: https://bolnew-sigma.vercel.app"
    echo ""
else
    echo ""
    echo "❌ Push failed. Please check:"
    echo "1. Git credentials are correct"
    echo "2. Remote repository is accessible"
    echo "3. You have push permissions"
    echo ""
    exit 1
fi
