# 🚀 Deployment Guide - AI Interview Bot

## Quick Deploy Options

### ⭐ Option 1: Render (Recommended - FREE)

**Get a public URL like: `https://your-ai-interviewer.onrender.com`**

#### Steps:

1. **Create Render Account:**
   - Go to: https://render.com
   - Sign up with GitHub (connect your mahimachauhan17/Bot repository)

2. **Create New Blueprint:**
   - Click "New +" → "Blueprint"
   - Select your `mahimachauhan17/Bot` repository
   - Render will automatically detect `render.yaml`
   - Click "Apply"

3. **Add Environment Variables:**
   After deployment starts, add these in Render dashboard:
   ```
   OPENAI_API_KEY=your-actual-openai-key
   FRONTEND_URL=https://your-frontend-name.onrender.com
   ```

4. **Wait 5-10 minutes** for first deployment

5. **Your App is Live!** 🎉
   - Frontend: `https://interviewer-ai-frontend.onrender.com`
   - Backend API: `https://interviewer-ai-backend.onrender.com`

**✅ FREE Tier Includes:**
- 750 hours/month free
- Automatic HTTPS
- MongoDB + Redis included
- Auto-deploy on git push

---

### 🐳 Option 2: Railway (Also FREE)

1. Go to: https://railway.app
2. Click "Deploy from GitHub"
3. Select `mahimachauhan17/Bot`
4. Railway auto-detects Docker setup
5. Add environment variables
6. Get URL: `https://your-app.up.railway.app`

---

### ☁️ Option 3: DigitalOcean App Platform

1. Go to: https://cloud.digitalocean.com/apps
2. Click "Create App"
3. Connect GitHub → Select `mahimachauhan17/Bot`
4. Choose "Docker Compose" deployment
5. Get URL: `https://your-app.ondigitalocean.app`

**Cost:** $5-12/month (not free but more reliable)

---

### 🌐 Option 4: Vercel (Frontend) + Render (Backend)

**Free Hybrid Solution:**

**Backend on Render:**
1. Deploy backend to Render (free)
2. Get URL: `https://your-backend.onrender.com`

**Frontend on Vercel:**
1. Go to: https://vercel.com
2. Import `mahimachauhan17/Bot`
3. Set root directory: `frontend`
4. Add env variable: `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api`
5. Get URL: `https://your-ai-bot.vercel.app`

---

## 🎯 EASIEST PATH (Recommended for Beginners):

1. **Push your code to GitHub** ✅ (Already done!)
2. **Go to Render.com**
3. **Sign up with GitHub**
4. **Click "New Blueprint"** → Select your repo
5. **Add OPENAI_API_KEY in dashboard**
6. **Wait 10 minutes** ⏰
7. **Get your public URL!** 🎉

---

## 📝 Before Deployment Checklist:

✅ Code is on GitHub (Done!)
✅ `.env` files are not committed (Done!)
✅ `render.yaml` is created (Done!)
✅ Docker files exist (Done!)
✅ Have your OpenAI API key ready

---

## 🔗 After Deployment:

You'll get URLs like:
- **Main App:** `https://interviewer-ai-frontend.onrender.com`
- **Admin Panel:** `https://interviewer-ai-backend.onrender.com/admin/`
- **API:** `https://interviewer-ai-backend.onrender.com/api/`

**Share one link with anyone in the world!** 🌍

---

## 💡 Need Help?

1. Make sure code is pushed to GitHub
2. Sign up on Render.com
3. Follow the 6 steps above
4. Let me know if you face any issues!

**Deployment Time:** ~10 minutes
**Cost:** FREE forever (with some limitations)
