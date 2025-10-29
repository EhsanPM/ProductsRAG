# 🛒 Grocery Store RAG Chatbot

A powerful RAG (Retrieval-Augmented Generation) application for grocery product search, built with **LangGraph**, **Streamlit**, and **OpenAI**.

## ✨ Features

- 🤖 **Conversational AI Assistant** - Natural language product search and recommendations
- 🔍 **Semantic Search** - Find products using OpenAI embeddings
- 🏃 **Athletic Products** - Specialized recommendations for athletes
- 🍝 **Recipe Suggestions** - Get ingredient recommendations for various recipes
- 📦 **Category Browsing** - Explore products by category
- 💾 **Vector Database** - Efficient product embeddings with ChromaDB
- 🎯 **LangGraph Tools** - Multiple specialized tools for different query types
- 💬 **Chat History** - Maintains conversation context
- 🎨 **Beautiful UI** - Clean Streamlit interface

## 🏗️ Architecture

The application uses a **LangGraph state machine** with the following components:

1. **Agent Node** - Decides which tools to use based on user query
2. **Tool Nodes** - Specialized functions for different operations:
   - `search_products` - Semantic search across all products
   - `get_products_by_category` - Filter by category
   - `suggest_products_for_recipe` - Recipe-based recommendations
   - `find_products_for_athletes` - Athletic nutrition products
3. **Vector Store** - ChromaDB with OpenAI embeddings (text-embedding-3-small)
4. **LLM** - GPT-4o-mini for response generation

## 📋 Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- OpenAI API key

## 🚀 Installation

### 1. Clone or navigate to the project directory

```bash
cd products_rag
```

### 2. Install Poetry (if not already installed)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. Install dependencies

```bash
poetry install
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Initialize the vector database (First run)

```bash
poetry run python product_rag.py
```

This will:
- Load products from `products.txt`
- Generate embeddings using OpenAI
- Create the ChromaDB vector store in `chroma_db_openai/`

## 🎮 Usage

### Running the Streamlit App

```bash
poetry run streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Running the CLI Test

To test the RAG system without the UI:

```bash
poetry run python product_rag.py
```

## 💡 Example Queries

Try asking questions like:

- "What products are good for athletes?"
- "Suggest some ingredients for a pasta recipe"
- "Show me dairy products"
- "What healthy snacks do you have?"
- "Find me some frozen vegetables"
- "I need ingredients for a salad"
- "Show me products under $3"
- "What breakfast items do you have?"

## 📁 Project Structure

```
products_rag/
├── app.py                  # Streamlit chatbot interface
├── product_rag.py          # Core RAG system with LangGraph
├── products.txt            # Product data (JSON lines)
├── pyproject.toml          # Poetry dependencies
├── .env                    # Environment variables (create this)
├── .env.example            # Template for environment variables
├── .gitignore             # Git ignore file
├── README.md              # This file
└── chroma_db_openai/      # Vector database (auto-generated)
```

## 🔧 Configuration

### Changing the OpenAI Model

Edit `product_rag.py`:

```python
# For embeddings
self.embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"  # or text-embedding-3-large
)

# For chat
self.llm = ChatOpenAI(
    model="gpt-4o-mini"  # or gpt-4, gpt-3.5-turbo
)
```

### Adjusting Search Results

Modify the `limit` parameter in tool functions:

```python
@tool
def search_products(query: str, limit: int = 5):  # Change default here
    ...
```

## 🛠️ Development

### Adding New Tools

Add new tools in `product_rag.py` within the `_create_tools()` method:

```python
@tool
def your_new_tool(param: str) -> str:
    """Tool description for the LLM"""
    # Your logic here
    return result
```

### Modifying the Product Schema

Update the `Product` class in `product_rag.py`:

```python
class Product(BaseModel):
    id: str
    name: str
    # Add new fields here
```

## 🔍 How It Works

1. **Initialization**:
   - Loads products from `products.txt`
   - Creates/loads vector store with OpenAI embeddings
   - Initializes LangGraph workflow with tools

2. **Query Processing**:
   - User asks a question in Streamlit
   - LangGraph agent analyzes the query
   - Agent decides which tool(s) to use
   - Tools execute and return results
   - LLM generates natural language response
   - Response displayed in chat interface

3. **Vector Search**:
   - Products are embedded with semantic information
   - User queries are embedded using the same model
   - ChromaDB finds most relevant products
   - Results are ranked by similarity

## 📊 Vector Database

The application creates a ChromaDB vector database on first run:

- **Location**: `chroma_db_openai/`
- **Embeddings**: OpenAI text-embedding-3-small (1536 dimensions)
- **Content**: Product name, brand, description, categories, and price
- **Persistence**: Database is saved locally and reused on subsequent runs

To rebuild the database, simply delete the `chroma_db_openai/` directory and run the app again.

## 🐛 Troubleshooting

> **📖 For detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

### Quick Fixes

#### ChromaDB Telemetry Error
```
Failed to send telemetry event CollectionQueryEvent...
```
This has been fixed in the code. If you still see it, delete and recreate the database:
```bash
rm -rf chroma_db_openai/
poetry run python product_rag.py
```

#### "Import errors" when starting

Make sure you've installed dependencies:
```bash
poetry install
```

### "OpenAI API key not found"

Check your `.env` file:
```bash
cat .env
# Should show: OPENAI_API_KEY=sk-...
```

### Vector store not loading

Delete and recreate:
```bash
rm -rf chroma_db_openai/
poetry run python product_rag.py
```

### Streamlit not opening

Check the port:
```bash
poetry run streamlit run app.py --server.port 8502
```

## 📦 Dependencies

Main dependencies (see `pyproject.toml` for full list):

- **streamlit**: Web UI framework
- **langgraph**: State machine and agent orchestration
- **langchain**: LLM framework
- **langchain-openai**: OpenAI integration
- **langchain-chroma**: ChromaDB vector store
- **python-dotenv**: Environment variable management
- **pydantic**: Data validation

## 🤝 Contributing

Feel free to:
- Add new tools for different query types
- Improve the UI/UX
- Add more product data
- Optimize embeddings and search

## 📝 License

MIT License - feel free to use this project as you wish!

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- UI powered by [Streamlit](https://streamlit.io/)
- Embeddings by [OpenAI](https://openai.com/)
- Vector store by [ChromaDB](https://www.trychroma.com/)

---

**Need help?** Check the example queries or explore the code comments for more details!
