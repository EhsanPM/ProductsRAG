# 🚀 Streamlit Cloud Deployment Guide

## Quick Deployment Checklist

### ✅ Prerequisites
- [ ] GitHub account
- [ ] OpenAI API key
- [ ] Repository pushed to GitHub

### 📦 Preparation

#### 1. Export Dependencies (Already Done!)
```bash
# Already exported to requirements.txt
# If you add new packages, run:
poetry add package-name
./deploy_prep.sh
```

#### 2. Verify Files Exist
```bash
# Run the deployment preparation script
./deploy_prep.sh
```

This will check:
- ✅ requirements.txt (exported from Poetry)
- ✅ products.txt (4,574 products)
- ✅ app.py (Streamlit interface)
- ✅ product_rag.py (RAG system)
- ✅ .streamlit/config.toml (configuration)

#### 3. Push to GitHub
```bash
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

---

## 🌐 Deploy on Streamlit Cloud

### Step 1: Visit Streamlit Cloud
Go to: **https://share.streamlit.io**

### Step 2: Sign In
- Click **"Sign in with GitHub"**
- Authorize Streamlit Cloud

### Step 3: Deploy New App
1. Click **"New app"** button
2. Fill in the form:
   - **Repository:** `EhsanPM/ProductsRAG`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** Choose a name (e.g., `grocery-rag-assistant`)

### Step 4: Add Secrets (CRITICAL!)
1. Click **"Advanced settings"**
2. Click **"Secrets"** section
3. Add the following:

```toml
OPENAI_API_KEY = "sk-proj-your-actual-key-here"
ANONYMIZED_TELEMETRY = "False"
```

**⚠️ IMPORTANT:** Replace `sk-proj-your-actual-key-here` with your real OpenAI API key!

### Step 5: Deploy
1. Click **"Deploy!"** button
2. Wait 2-5 minutes for deployment

---

## ⏱️ What Happens During Deployment

### First Deployment (3-5 minutes total):

#### Phase 1: Build (1-2 minutes)
```
[00:00] Cloning repository from GitHub...
[00:15] Installing dependencies from requirements.txt...
[01:30] Dependencies installed ✅
```

#### Phase 2: First Run Setup (2-3 minutes)
```
[01:31] Starting Streamlit app...
[01:32] Detecting first run (no ChromaDB exists)...
[01:33] Loading 4,574 products from products.txt...
[01:35] Creating OpenAI embeddings... (slow part)
[03:45] Building ChromaDB vector index...
[04:15] Vector database created successfully! ✅
[04:16] App is live! 🎉
```

**Your app URL:** `https://your-app-name.streamlit.app`

#### Phase 3: Subsequent Visits (5-10 seconds)
```
[00:00] Loading existing ChromaDB...
[00:03] ChromaDB loaded ✅
[00:05] App ready! ⚡
```

---

## 🎯 What You'll See

### On First Deployment:

When you visit your app URL, you'll see:

```
🚀 First-Time Setup in Progress

This is the first time running the app. We're setting up:

1. 📚 Loading 4,574 grocery products from database
2. 🧠 Creating AI embeddings using OpenAI
3. 💾 Building vector search index with ChromaDB

This takes 2-3 minutes and only happens once.

Future app starts will be instant! ⚡

[Progress bar showing 60%]
🔧 Finalizing setup...
```

### After Setup Completes:

```
✅ Setup Complete! The app is now ready to use.

[App refreshes automatically]

🛒 Grocery Store Assistant Chat
Ask me anything about our products!

💡 Quick Start Questions:
[🏃 Athletic Products] [🍝 Pasta Recipe] [🥗 Healthy Snacks]
```

---

## 📊 Monitoring Your Deployment

### View Build Logs
1. Go to your app dashboard
2. Click **"Manage app"**
3. View **"Logs"** tab
4. Watch real-time deployment progress

### Check App Status
- **Green dot:** App is running ✅
- **Yellow dot:** App is starting ⏳
- **Red dot:** App has errors ❌

---

## 🔧 Troubleshooting

### Issue: "OpenAI API key not found"
**Solution:**
1. Go to app settings
2. Click **"Secrets"**
3. Add `OPENAI_API_KEY` with your key
4. Click **"Save"**
5. App will auto-restart

### Issue: "Module not found"
**Solution:**
1. Verify `requirements.txt` is in repository root
2. Run `./deploy_prep.sh` to regenerate
3. Commit and push changes
4. Streamlit Cloud will auto-redeploy

### Issue: "products.txt not found"
**Solution:**
```bash
# Make sure products.txt is committed
git add products.txt
git commit -m "Add products file"
git push
```

### Issue: "First setup takes too long"
**Expected behavior!** First setup:
- Creates embeddings for 4,574 products
- Takes 2-3 minutes (OpenAI API rate limits)
- Only happens once
- Future visits are instant (3-5 seconds)

### Issue: "ChromaDB warnings in logs"
**Not a problem!** Warnings are suppressed in the UI. The app works perfectly despite these warnings.

---

## 🔄 Updating Your Deployed App

### After Making Code Changes:

```bash
# 1. Make your changes locally
# 2. Test locally
poetry run streamlit run app.py

# 3. If you added dependencies, export them
./deploy_prep.sh

# 4. Commit and push
git add .
git commit -m "Update feature X"
git push origin main

# 5. Streamlit Cloud auto-deploys!
```

Streamlit Cloud automatically redeploys when you push to `main` branch.

---

## 💰 Cost Considerations

### Streamlit Cloud
- **Free tier:** Unlimited public apps
- **Private apps:** $20/month

### OpenAI API Costs (per query)
- **Embeddings:** ~$0.0001 per query
- **GPT-4o-mini:** ~$0.002 per query
- **Total:** ~$0.0021 per user query

**Monthly estimates:**
- 100 queries/day = ~$6/month
- 500 queries/day = ~$30/month
- 1,000 queries/day = ~$60/month

**Tip:** Set usage limits in your OpenAI dashboard!

---

## 📱 Sharing Your App

Once deployed, share your app URL:
```
https://your-app-name.streamlit.app
```

### Custom Domain (Optional)
1. Go to app settings
2. Click **"Custom domain"**
3. Add your domain (requires DNS setup)

---

## 🎉 Success!

Your RAG chatbot is now live on Streamlit Cloud!

**Features:**
- ✅ Automatic HTTPS
- ✅ Auto-scaling
- ✅ Auto-restart on crashes
- ✅ Persistent storage (ChromaDB saved)
- ✅ GitHub auto-deploy
- ✅ Usage analytics

**Next steps:**
- Share your app with users
- Monitor usage in Streamlit dashboard
- Add more features and push updates
- Watch OpenAI API usage

---

## 📞 Support

**Streamlit Community:**
- Forum: https://discuss.streamlit.io
- Docs: https://docs.streamlit.io

**Your App Dashboard:**
- https://share.streamlit.io/[your-username]/ProductsRAG

**OpenAI Dashboard:**
- https://platform.openai.com/usage

---

**Happy Deploying! 🚀**
