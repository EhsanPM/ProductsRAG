# Grocery Store RAG Chatbot

A conversational AI assistant for searching grocery products. Built with LangGraph, Streamlit, and OpenAI.

## Overview

This application provides natural language search over a grocery product database using retrieval-augmented generation. It supports semantic search, category filtering, recipe suggestions, and athletic nutrition recommendations.

## Prerequisites

- Python 3.10+
- Poetry
- OpenAI API key

## Installation

Install dependencies using Poetry:

```bash
poetry install
```

Create a `.env` file with your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the Streamlit application:

```bash
poetry run streamlit run app.py
```

The application will automatically create the vector database on first run.

## Project Structure

```
products_rag/
├── app.py              # Streamlit interface
├── product_rag.py      # Core RAG system
├── products.txt        # Product database
├── pyproject.toml      # Dependencies
└── chroma_db_openai/   # Vector store (auto-generated)
```

## How It Works

The system uses LangGraph to orchestrate an agent with multiple tools. When you ask a question, the agent selects the appropriate tool, retrieves relevant products from the vector database, and generates a natural language response using GPT-4o-mini.

## License

MIT
