# DEPLOYMENT GUIDE

## Quick Start - Deploy to Vercel + Render

### Step 1: Get Your OpenRouter API Key (2 min)
1. Go to https://openrouter.ai/
2. Sign up with Google
3. Go to Keys tab (https://openrouter.ai/keys)
4. Create a new key - copy it

### Step 2: Deploy Backend to Render (5 min)

1. Go to https://render.com and sign up with GitHub
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Settings:
   - **Name**: code-review-agent-backend
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `gunicorn backend.main:app --bind 0.0.0.0:$PORT`
5. Add Environment Variable:
   - Key: `OPENROUTER_API_KEY`
   - Value: Your OpenRouter API key
6. Click "Create Web Service"
7. Wait for deployment (3-5 minutes)
8. Copy your deployed URL (e.g., `https://code-review-agent-backend.onrender.com`)

### Step 3: Deploy Frontend to Vercel (3 min)

1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "New Project"
4. Import your GitHub repository
5. Framework preset: **Vite**
6. Root Directory: `frontend`
7. Build command: `npm run build`
8. Output directory: `dist`
9. Environment variables:
   - Key: `VITE_API_URL`
   - Value: Your Render backend URL (from Step 2)
10. Click "Deploy"
11. Wait 1-2 minutes
12. Your app is LIVE! Copy the Vercel URL

## Testing Your Deployment

1. Open your Vercel URL in browser
2. Paste sample code:
```python
def hello():
    x = 1
    y = 2
    return x
```
3. Click "Review Code"
4. You should see AI-generated code review!

## If Backend Doesn't Work

Try these free alternatives:

### Deploy to Railway (Even Easier)
1. Go to https://railway.app
2. Connect GitHub
3. Add your repo
4. Add environment variable `OPENROUTER_API_KEY`
5. Railway auto-deploys!

### Deploy to Replit
1. Go to https://replit.com
2. Create new Repl → Import from GitHub
3. Add `.env` with OpenRouter key
4. Click "Run"

## Getting Loem Video URL

Use Loom for 1-minute screen recording:
1. Install Loom Chrome extension
2. Share your screen with app running
3. Explain what it does (30 seconds)
4. Show code review in action (20 seconds)
5. Share Loom link in submission

## Troubleshooting

**API not responding?**
- Check OpenRouter API key is correct
- Check environment variable is set
- Check backend logs in Render/Railway dashboard

**Frontend shows error?**
- Clear browser cache (Ctrl+Shift+Delete)
- Check VITE_API_URL environment variable is set correctly
- Check backend URL in Vercel environment variables

**Local testing not working?**
- Run `pip install -r backend/requirements.txt`
- Run `cd frontend && npm install`
- Start backend: `python backend/main.py`
- Start frontend: `cd frontend && npm run dev`
- Visit http://localhost:5173
