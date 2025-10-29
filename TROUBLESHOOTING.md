# Troubleshooting Guide

## Common Issues and Solutions

### ❌ ChromaDB Telemetry Error

**Error Message:**
```
Failed to send telemetry event CollectionQueryEvent: capture() takes 1 positional argument but 3 were given
```

**Cause:** ChromaDB telemetry compatibility issue with certain versions.

**Solution:** This has been fixed in the code. The application now disables telemetry by default. If you still see this error:

1. Make sure you're using the latest version of the code
2. Delete the vector database and recreate it:
   ```bash
   rm -rf chroma_db_openai/
   poetry run python product_rag.py
   ```

### ❌ OpenAI API Key Not Found

**Error Message:**
```
OpenAI API key not found
```

**Solution:**
1. Make sure you have a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your actual API key:
   ```env
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

3. Restart the application

### ❌ Import Errors

**Error Message:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
Install dependencies with Poetry:
```bash
poetry install
```

If Poetry is not installed:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### ❌ Vector Database Not Loading

**Error Message:**
```
No vector database found
```

**Solution:**
1. Run the initialization script:
   ```bash
   poetry run python product_rag.py
   ```

2. Wait for the vector database to be created (30-60 seconds)

3. Then run the Streamlit app:
   ```bash
   poetry run streamlit run app.py
   ```

### ❌ Slow Responses

**Symptom:** Queries take a long time to respond

**Possible Causes:**
1. **First query** - Creating the vector database takes time (~30-60 seconds)
2. **OpenAI API** - Normal response time is 2-5 seconds
3. **Internet connection** - Check your network connection

**Solutions:**
- Be patient on first run
- Check your internet connection
- Verify OpenAI API status at status.openai.com

### ❌ Port Already in Use

**Error Message:**
```
Port 8501 is already in use
```

**Solution:**
Use a different port:
```bash
poetry run streamlit run app.py --server.port 8502
```

Or kill the process using the port:
```bash
lsof -ti:8501 | xargs kill -9
```

### ❌ Permission Denied (start.sh)

**Error Message:**
```
Permission denied: ./start.sh
```

**Solution:**
Make the script executable:
```bash
chmod +x start.sh
```

### ❌ ChromaDB PersistentClient Error

**Error Message:**
```
ValueError: Could not connect to tenant default_tenant
```

**Solution:**
Delete and recreate the vector database:
```bash
rm -rf chroma_db_openai/
poetry run python product_rag.py
```

### ❌ Empty Responses from LLM

**Symptom:** The chatbot returns empty or very short responses

**Possible Causes:**
1. OpenAI API rate limits
2. Invalid API key
3. Network issues

**Solutions:**
1. Check your OpenAI API key is valid and has credits
2. Check OpenAI API status
3. Wait a moment and try again

### ❌ Products Not Found

**Symptom:** Queries return "no products found" even though products.txt has data

**Solution:**
1. Verify products.txt exists and has content:
   ```bash
   cat products.txt | head -5
   ```

2. Rebuild the vector database:
   ```bash
   rm -rf chroma_db_openai/
   poetry run python product_rag.py
   ```

3. Check for JSON parsing errors in the console output

## Debug Mode

To run with more verbose output:

```bash
export DEBUG=1
poetry run python product_rag.py
```

## Getting More Help

1. **Check the logs** - Look at the terminal output for error messages
2. **Read the error message** - Most errors are self-explanatory
3. **Check your .env file** - Make sure API keys are correct
4. **Verify dependencies** - Run `poetry install` again
5. **Check OpenAI status** - Visit status.openai.com
6. **Review README.md** - Full documentation available

## System Requirements Check

Verify your system meets requirements:

```bash
# Check Python version (should be 3.10+)
python --version

# Check Poetry is installed
poetry --version

# Check internet connectivity
curl -I https://api.openai.com

# Check disk space (need ~500MB)
df -h .
```

## Clean Installation

If all else fails, try a clean installation:

```bash
# 1. Remove virtual environment
poetry env remove python

# 2. Remove vector database
rm -rf chroma_db_openai/

# 3. Reinstall dependencies
poetry install

# 4. Initialize vector database
poetry run python product_rag.py

# 5. Run the app
poetry run streamlit run app.py
```

## Still Having Issues?

If you're still experiencing problems:

1. Check that your `.env` file has the correct API key
2. Verify you have an active internet connection
3. Make sure you have OpenAI API credits
4. Try running the test script to isolate the issue:
   ```bash
   poetry run python product_rag.py
   ```

---

**Last Updated:** October 29, 2025
