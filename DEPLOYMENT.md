# Deployment Guide

This application can be deployed in several ways. Choose the option that best fits your needs:

## 🚀 Option 1: Full Stack on Railway (Recommended)

Railway is perfect for this app because it supports both Python backends and can handle large models.

### Steps:
1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Deploy:**
   ```bash
   railway deploy
   ```

4. **Set environment variables:**
   ```bash
   railway variables set MODEL_PATH=/app/model
   ```

## 🌐 Option 2: Hybrid Deployment (Vercel + Railway/Heroku)

Deploy frontend on Vercel and backend on Railway/Heroku.

### Frontend (Vercel):
1. **Push to GitHub** (if not already)
2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import your repository
   - Set build directory to `frontend`
   - Deploy

### Backend (Railway/Heroku):
1. **Deploy backend to Railway:**
   ```bash
   cd backend
   railway deploy
   ```

2. **Update frontend API URL:**
   - In `frontend/src/components/MeshGenerator.js`
   - Change API calls from `/api/` to your Railway URL

## 🐳 Option 3: Docker Deployment (Any Platform)

### Railway with Docker:
```bash
# Railway will auto-detect Dockerfile
railway deploy
```

### Heroku with Docker:
1. **Install Heroku CLI**
2. **Login and create app:**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Deploy:**
   ```bash
   heroku container:push web
   heroku container:release web
   ```

### DigitalOcean App Platform:
1. **Connect GitHub repository**
2. **Select Docker deployment**
3. **Deploy automatically**

## 🏠 Option 4: Local/VPS Deployment

### Using Docker Compose:
```bash
# Clone and deploy
git clone <your-repo>
cd mesh-generator
docker-compose up -d
```

### Manual deployment:
```bash
# Install dependencies
pip install -r requirements.txt
cd frontend && npm install && npm run build && cd ..

# Start backend
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## 🔧 Environment Variables

Set these in your deployment platform:

```bash
MODEL_PATH=/app/model
PYTHONPATH=/app
PORT=8000  # For platforms that require PORT
```

## 📊 Platform Comparison

| Platform | Frontend | Backend | Model Support | Cost | Ease |
|----------|----------|---------|---------------|------|------|
| Railway | ✅ | ✅ | ✅ | $5/month | ⭐⭐⭐⭐⭐ |
| Vercel + Railway | ✅ | ✅ | ✅ | $5/month | ⭐⭐⭐⭐ |
| Heroku | ✅ | ✅ | ❌ (size limit) | $7/month | ⭐⭐⭐ |
| DigitalOcean | ✅ | ✅ | ✅ | $12/month | ⭐⭐⭐ |
| Docker VPS | ✅ | ✅ | ✅ | $5/month | ⭐⭐ |

## 🎯 Recommended: Railway (Full Stack)

Railway is the best choice because:
- ✅ Supports large Python applications
- ✅ Can handle your ML model
- ✅ Automatic deployments from GitHub
- ✅ Built-in database support
- ✅ Reasonable pricing
- ✅ Easy environment management

### Quick Railway Deployment:
```bash
# One command deployment
railway deploy
```

Your app will be live at: `https://your-app-name.railway.app`
