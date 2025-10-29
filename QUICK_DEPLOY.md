# 🎯 Quick Reference - Streamlit Cloud Deployment

## ⚡ One-Command Preparation

```bash
./deploy_prep.sh
```

This checks everything and exports dependencies.

---

## 📋 Deployment Checklist

### Before Deploying:
- [ ] Run `./deploy_prep.sh`
- [ ] Verify all checks pass
- [ ] Push to GitHub: `git push origin main`

### On Streamlit Cloud:
1. Go to https://share.streamlit.io
2. Click "New app"
3. **Repository:** `EhsanPM/ProductsRAG`
4. **Branch:** `main`
5. **Main file:** `app.py`
6. **Add Secrets:**
   ```toml
   OPENAI_API_KEY = "sk-your-key-here"
   ANONYMIZED_TELEMETRY = "False"
   ```
7. Click "Deploy!"

---

## ⏱️ Expected Times

| Phase | Duration | What Happens |
|-------|----------|--------------|
| Build | 1-2 min | Install dependencies |
| First Run | 2-3 min | Create ChromaDB with embeddings |
| **Total** | **3-5 min** | One-time setup |
| Future Loads | 5-10 sec | Load existing ChromaDB |

---

## 🔄 Update Workflow

```bash
# 1. Make changes locally
# Edit files...

# 2. Test locally (optional)
poetry run streamlit run app.py

# 3. Update dependencies if needed
poetry add new-package
./deploy_prep.sh

# 4. Push to GitHub
git add .
git commit -m "Description of changes"
git push origin main

# 5. Streamlit Cloud auto-deploys!
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not found" | Add `OPENAI_API_KEY` to Streamlit secrets |
| "Module not found" | Run `./deploy_prep.sh` and push `requirements.txt` |
| "products.txt missing" | `git add products.txt && git push` |
| "Setup too slow" | Normal! First run takes 2-3 min, then instant |
| "ChromaDB warnings" | Ignore - they're suppressed in UI |

---

## 📊 Important Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Dependencies (auto-generated) |
| `products.txt` | Product data (4,574 items) |
| `app.py` | Streamlit UI |
| `product_rag.py` | RAG system |
| `.streamlit/config.toml` | Streamlit configuration |
| `deploy_prep.sh` | Deployment checker |
| `DEPLOYMENT.md` | Full deployment guide |

---

## 🌐 Your App URLs

**Streamlit Dashboard:**
```
https://share.streamlit.io
```

**Your App (after deployment):**
```
https://your-app-name.streamlit.app
```

**OpenAI Dashboard:**
```
https://platform.openai.com/usage
```

---

## 💰 Estimated Costs

**Per Query:** ~$0.002
**Monthly (100 queries/day):** ~$6
**Monthly (500 queries/day):** ~$30

Set limits at: https://platform.openai.com/settings/organization/limits

---

## 🆘 Need Help?

**Full Guide:** See `DEPLOYMENT.md`
**Streamlit Docs:** https://docs.streamlit.io
**Streamlit Forum:** https://discuss.streamlit.io

---

## ✅ Current Status

✅ Dependencies exported to `requirements.txt`
✅ First-run setup code added to `app.py`
✅ Streamlit config created
✅ All files verified
✅ **Ready to deploy!**

**Next Step:** Push to GitHub and deploy on Streamlit Cloud! 🚀
