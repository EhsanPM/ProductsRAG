#!/bin/bash
# Quick start script for the Grocery Store RAG Chatbot

echo "🛒 Grocery Store RAG Chatbot - Setup"
echo "===================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
    echo ""
    read -p "Press enter after you've added your API key to .env..."
fi

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed!"
    echo "Install it with: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

echo "📦 Installing dependencies..."
poetry install

echo ""
echo "🔄 Initializing vector database (this may take a minute)..."
poetry run python product_rag.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Streamlit app..."
poetry run streamlit run app.py
