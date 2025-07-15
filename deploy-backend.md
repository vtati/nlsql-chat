# Backend Deployment Guide

## Option 1: Railway with Backend-Only Repo

1. **Create a new repository** for just the backend:
   - Copy all files from `backend/` folder to root of new repo
   - Push to GitHub as `nlsql-backend`

2. **Deploy on Railway**:
   - Connect the backend-only repository
   - Railway will auto-detect Python and requirements.txt
   - Add environment variable: `OPENAI_API_KEY`

## Option 2: Use Railway CLI (Easier)

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and deploy**:
   ```bash
   railway login
   cd backend
   railway init
   railway up
   ```

3. **Add environment variables**:
   ```bash
   railway variables set OPENAI_API_KEY=your_key_here
   ```

## Option 3: Use Render (Alternative)

1. Go to https://render.com
2. Connect GitHub repository
3. Create Web Service
4. Set:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `OPENAI_API_KEY`