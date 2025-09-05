#!/bin/bash

# Railway Deployment Script
echo "🚀 Deploying to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI is not installed."
    echo "📦 Install it with: npm install -g @railway/cli"
    exit 1
fi

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway first:"
    railway login
fi

# Deploy the application
echo "🚀 Deploying application..."
railway deploy

# Get the deployment URL
echo "⏳ Getting deployment URL..."
DEPLOY_URL=$(railway domain)

if [ ! -z "$DEPLOY_URL" ]; then
    echo "✅ Deployment successful!"
    echo "🌐 Your app is live at: https://$DEPLOY_URL"
    echo "📊 API docs: https://$DEPLOY_URL/docs"
else
    echo "⚠️ Deployment completed, but couldn't get URL."
    echo "Check your Railway dashboard for the URL."
fi

echo "🎉 Deployment complete!"
