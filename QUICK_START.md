# Quick Reference Guide

## 🚀 Quick Start

```bash
# 1. Copy and edit .env
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 2. Install dependencies
poetry install

# 3. Run the app
./start.sh
```

## 💬 Example Questions to Ask

### 🏃 Athletic & Healthy
- "What products are good for athletes?"
- "Show me high-protein foods"
- "Find healthy snacks"
- "What organic options do you have?"

### 🍝 Recipe Ideas
- "Suggest ingredients for a pasta recipe"
- "What do I need for a salad?"
- "Products for making breakfast"
- "Items for a soup recipe"

### 📦 Category Browsing
- "Show me dairy products"
- "What snacks do you have?"
- "Display frozen foods"
- "List breakfast cereals"

### 💰 Price Queries
- "What are the cheapest products?"
- "Show me items under $3"
- "Compare yogurt prices"

## 🛠️ Commands

### Start the App
```bash
poetry run streamlit run app.py
```

### Test RAG System
```bash
poetry run python product_rag.py
```

### Rebuild Vector Database
```bash
rm -rf chroma_db_openai/
poetry run python product_rag.py
```

### Install Dependencies
```bash
poetry install
```

## 📁 Important Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit chatbot UI |
| `product_rag.py` | Core RAG system |
| `products.txt` | Product database |
| `.env` | API keys (create this!) |
| `pyproject.toml` | Dependencies |

## 🔧 Troubleshooting

### Problem: "OpenAI API key not found"
**Solution**: Create `.env` file with `OPENAI_API_KEY=sk-...`

### Problem: Import errors
**Solution**: Run `poetry install`

### Problem: Streamlit won't start
**Solution**: Try a different port:
```bash
poetry run streamlit run app.py --server.port 8502
```

### Problem: Slow responses
**Solution**: This is normal - OpenAI API takes 2-5 seconds

### Problem: Vector database missing
**Solution**: Run `poetry run python product_rag.py`

## 🎯 Project Structure

```
products_rag/
├── app.py                  # 🎨 Streamlit UI
├── product_rag.py          # 🧠 RAG brain
├── products.txt            # 📦 Product data
├── pyproject.toml          # 📋 Dependencies
├── .env                    # 🔑 API keys
├── README.md               # 📖 Full docs
├── QUICK_START.md          # ⚡ This file
└── chroma_db_openai/       # 💾 Vector DB
```

## 🌟 Key Features

- ✅ Semantic product search
- ✅ Recipe suggestions
- ✅ Category filtering
- ✅ Athletic product recommendations
- ✅ Conversational interface
- ✅ Chat history
- ✅ Quick action buttons

## 📞 Getting Help

1. Check the [README.md](README.md) for detailed docs
2. Look at example queries above
3. Review error messages carefully
4. Make sure `.env` file exists with valid API key

## 🎮 Tips for Best Results

1. **Be specific**: "Show me high-protein yogurt" is better than just "yogurt"
2. **Use natural language**: Ask questions like you would to a person
3. **Try variations**: If one query doesn't work, rephrase it
4. **Use categories**: Mention category names like "snacks", "dairy", "frozen"
5. **Ask follow-ups**: The chatbot remembers conversation history

## ⚡ Performance Tips

- First query creates the vector database (~30-60 seconds)
- Subsequent queries are much faster (2-5 seconds)
- Clear chat history if responses become irrelevant
- Restart app if it becomes slow

## 📊 System Requirements

- **Python**: 3.10 or higher
- **RAM**: At least 2GB free
- **Disk**: ~500MB for dependencies and database
- **Internet**: Required for OpenAI API calls

---

**Need more help?** See [README.md](README.md) for comprehensive documentation!
