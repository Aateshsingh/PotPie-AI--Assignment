# QUICK REFERENCE - Execute These Steps

## ⏰ NEXT 5 MINUTES: Get OpenRouter API Key

```bash
# 1. Visit: https://openrouter.ai/auth/signin
# 2. Click "Sign in with Google"
# 3. Go to: https://openrouter.ai/keys
# 4. Create key
# 5. Copy the key (you'll need it below)
```

## ⏰ 5-10 MINUTES: Deploy Backend (Render - Easiest)

1. **Go to**: https://render.com
2. **Sign up** with GitHub (authorize it)
3. **Click**: "New +" → "Web Service"
4. **Connect**: Your GitHub repo
5. **Fill in**:
   - Name: `code-review-agent-backend`
   - Runtime: `Python 3`
   - Build: `pip install -r backend/requirements.txt`
   - Start: `gunicorn backend.main:app --bind 0.0.0.0:$PORT`
6. **Add Environment Variable**:
   - Key: `OPENROUTER_API_KEY`
   - Value: [Paste your key from step above]
7. **Click**: "Create Web Service"
8. **Wait** 3-5 minutes for deployment
9. **Copy URL** when it shows "Your service is live" (e.g., `https://code-review-agent-backend.onrender.com`)

## ⏰ 10-15 MINUTES: Deploy Frontend (Vercel)

1. **Go to**: https://vercel.com
2. **Sign up** with GitHub
3. **Click**: "Add New..." → "Project"
4. **Import** your GitHub repository
5. **Framework**: Select `Vite`
6. **Root Directory**: Set to `frontend`
7. **Add Environment Variable**:
   - Name: `VITE_API_URL`
   - Value: [Render URL from previous step]
8. **Click**: "Deploy"
9. **Wait** 1-2 minutes
10. **Share URL** when it says "Domains" (e.g., `https://your-project.vercel.app`)

## ⏰ 10 MINUTES: Test Your App

1. **Open** the Vercel URL in browser
2. **Paste** this Python code:
```python
def calculate_sum(numbers):
    total = 0
    for n in numbers:
        total = total + n
    return total
```
3. **Click** "🔍 Review Code"
4. **Wait** 3-5 seconds
5. **You should see** AI review and suggestions!

## ⏰ 5 MINUTES: Record Loom Video

1. **Install** Loom Chrome extension: https://www.loom.com/download
2. **Open** your Vercel app in Chrome
3. **Open** your GitHub repo in another tab
4. **Open** your Render backend dashboard
5. **Click** Loom icon → "Start recording"
6. **Make sure webcam is ON** (face visible!)
7. **Show your face** and say:
   - "Hi, I'm [Your Name]"
   - "This is my Code Review Agent built with Pydantic AI"
   - "It analyzes code and provides AI suggestions"
8. **Paste** sample code and click "Review Code"
9. **Wait** for result, show the output
10. **Switch** to GitHub tab, show repo structure
11. **Say**: "Everything is deployed and working!"
12. **Click** "Stop recording"
13. **Click** "Share" → "Copy link" (make it public)
14. **Save** the Loom link

## ⏰ SUBMISSION CHECKLIST

Before submitting, you need:

```
☐ Live Vercel URL (your deployed app)
☐ GitHub repo URL (public, not private)
☐ Loom video URL (public link, face visible)
☐ Resume PDF or text
```

That's it! Everything is ready to submit.

## TROUBLESHOOTING QUICK FIXES

**"Backend not responding"**
→ Check Render logs, make sure OPENROUTER_API_KEY env var is set

**"Frontend shows error"**
→ Check VITE_API_URL in Vercel environment variables

**"Loom won't record"**
→ Make sure Chrome extension is installed and camera permission granted

**"API key invalid"**
→ Generate a new one at https://openrouter.ai/keys

**"Vercel build fails"**
→ Check `frontend/` has `package.json` and `vite.config.js`

## DEFAULT MODELS (Free Tier)

Use any of these in backend/main.py line 34:
- `openrouter/meta-llama/llama-2-7b-chat` ✅ FREE
- `openrouter/mistralai/mistral-7b` ✅ FREE
- `openrouter/openai/gpt-3.5-turbo` (credits available)

## GITHUB PUSH (If you made changes)

```bash
cd "/Users/aateshsingh/Desktop/PotPie AI  Assignment"
git add .
git commit -m "Deploy Code Review Agent"
git remote add origin https://github.com/YOUR_USERNAME/code-review-agent
git push -u origin main
```

---

**You're ready! 🚀 Submit when deployments are live!**
