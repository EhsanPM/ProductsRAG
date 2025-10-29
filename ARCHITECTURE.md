# Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Grocery Store RAG System                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Streamlit App (app.py)                   │  │
│  │  • Chat interface                                         │  │
│  │  • Session management                                     │  │
│  │  • Quick action buttons                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph RAG System                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              ProductRAG (product_rag.py)                  │  │
│  │                                                            │  │
│  │  ┌─────────────┐      ┌────────────────────────────┐    │  │
│  │  │   Agent     │      │      Tool Nodes            │    │  │
│  │  │   Node      │─────→│                            │    │  │
│  │  │             │      │  • search_products         │    │  │
│  │  │ Decides     │      │  • get_products_by_category│    │  │
│  │  │ which tool  │      │  • suggest_for_recipe      │    │  │
│  │  │ to use      │      │  • find_for_athletes       │    │  │
│  │  └─────────────┘      └────────────────────────────┘    │  │
│  │         ↓                        ↓                       │  │
│  │  ┌─────────────────────────────────────────────────┐    │  │
│  │  │          GPT-4o-mini (Response Gen)             │    │  │
│  │  └─────────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Vector Store Layer                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                ChromaDB (chroma_db_openai/)               │  │
│  │                                                            │  │
│  │  • Stores product embeddings                              │  │
│  │  • Similarity search                                      │  │
│  │  • Persistent storage                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                               ↑                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │    OpenAI Embeddings (text-embedding-3-small)            │  │
│  │    • 1536 dimensions                                      │  │
│  │    • Semantic understanding                               │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                         Data Layer                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              products.txt (JSON Lines)                    │  │
│  │                                                            │  │
│  │  • 50+ grocery products                                   │  │
│  │  • Name, brand, description, price, categories            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘


══════════════════════════════════════════════════════════════════
                          Query Flow
══════════════════════════════════════════════════════════════════

1. User Input
   └─→ "What products are good for athletes?"

2. Streamlit App
   └─→ Passes query to ProductRAG.query()

3. LangGraph Agent
   ├─→ Analyzes query with GPT-4o-mini
   ├─→ Decides to use: find_products_for_athletes tool
   └─→ Executes tool

4. Tool Execution
   ├─→ Searches vector store: "high protein lean meat"
   ├─→ Searches vector store: "greek yogurt protein"
   ├─→ Searches vector store: "organic vegetables"
   └─→ Combines results

5. Vector Store
   ├─→ Embeds queries with OpenAI
   ├─→ Finds similar products
   └─→ Returns top matches

6. Tool Result
   └─→ Returns JSON with product details

7. LLM Response Generation
   └─→ GPT-4o-mini creates natural language response

8. Response to User
   └─→ "Here are some great products for athletes:
        • Ground Turkey (21g protein)
        • Greek Yogurt (high protein)
        • Salmon Fillets (omega-3)
        ..."


══════════════════════════════════════════════════════════════════
                       State Machine Flow
══════════════════════════════════════════════════════════════════

    START
      ↓
   ┌────────┐
   │ Agent  │ ← Tool results loop back
   │  Node  │
   └────────┘
      ↓
   Has tool calls?
      ├─→ YES → ┌──────────┐
      │         │   Tool   │
      │         │   Node   │
      │         └──────────┘
      │              ↓
      │         Execute tool
      │              ↓
      │         Return results ─┘ (back to Agent)
      │
      └─→ NO → END (return response)


══════════════════════════════════════════════════════════════════
                    Component Interactions
══════════════════════════════════════════════════════════════════

┌────────────┐         ┌────────────┐         ┌────────────┐
│  Streamlit │────────→│  LangGraph │────────→│  OpenAI    │
│    UI      │         │    Agent   │         │    API     │
└────────────┘         └────────────┘         └────────────┘
      ↑                      ↓                       ↓
      │                ┌────────────┐         ┌────────────┐
      │                │   Tools    │         │ Embeddings │
      │                └────────────┘         └────────────┘
      │                      ↓                       ↓
      │                ┌────────────┐         ┌────────────┐
      └────────────────│  ChromaDB  │←────────│  Products  │
                       │   Vector   │         │    Data    │
                       └────────────┘         └────────────┘


══════════════════════════════════════════════════════════════════
                      Technology Stack
══════════════════════════════════════════════════════════════════

Layer              Technology              Purpose
───────────────────────────────────────────────────────────────────
Frontend           Streamlit               Chat interface
Orchestration      LangGraph               Agent workflow
LLM                GPT-4o-mini            Response generation
Embeddings         text-embedding-3-small  Semantic search
Vector DB          ChromaDB                Storage & retrieval
Data Format        JSON Lines              Product storage
Env Management     python-dotenv           API key config
Package Manager    Poetry                  Dependencies
───────────────────────────────────────────────────────────────────
