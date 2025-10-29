#!/bin/bash
# Deployment preparation script for Streamlit Cloud
# Run this before deploying to ensure requirements.txt is up to date

set -e  # Exit on error

echo "🚀 Preparing for Streamlit Cloud Deployment"
echo "============================================"
echo ""

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed!"
    echo "   Install it with: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

echo "✅ Poetry found"
echo ""

# Export dependencies
echo "📦 Exporting Poetry dependencies to requirements.txt..."
poetry export --format requirements.txt --output requirements.txt --without-hashes

if [ $? -eq 0 ]; then
    echo "✅ requirements.txt created successfully!"
else
    echo "❌ Failed to export dependencies"
    exit 1
fi

echo ""
echo "📋 Checking important files..."

# Check if products.txt exists
if [ -f "products.txt" ]; then
    echo "✅ products.txt found"
    PRODUCT_COUNT=$(wc -l < products.txt)
    echo "   Contains $PRODUCT_COUNT products"
else
    echo "❌ products.txt not found!"
    exit 1
fi

# Check if app.py exists
if [ -f "app.py" ]; then
    echo "✅ app.py found"
else
    echo "❌ app.py not found!"
    exit 1
fi

# Check if product_rag.py exists
if [ -f "product_rag.py" ]; then
    echo "✅ product_rag.py found"
else
    echo "❌ product_rag.py not found!"
    exit 1
fi

# Check if .streamlit/config.toml exists
if [ -f ".streamlit/config.toml" ]; then
    echo "✅ .streamlit/config.toml found"
else
    echo "⚠️  .streamlit/config.toml not found (optional)"
fi

echo ""
echo "📊 Git Status:"
git status --short

echo ""
echo "✅ All checks passed! Ready for deployment!"
echo ""
echo "Next steps:"
echo "  1. Review changes: git diff requirements.txt"
echo "  2. Stage files:    git add requirements.txt .streamlit/ app.py"
echo "  3. Commit:         git commit -m 'Prepare for Streamlit Cloud deployment'"
echo "  4. Push:           git push origin main"
echo ""
echo "Then deploy on Streamlit Cloud:"
echo "  🌐 https://share.streamlit.io"
echo ""
echo "⚠️  Remember to add your OpenAI API key in Streamlit Cloud secrets:"
echo "    OPENAI_API_KEY = \"sk-your-key-here\""
echo "    ANONYMIZED_TELEMETRY = \"False\""
