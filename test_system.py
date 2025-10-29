#!/usr/bin/env python3
"""
Quick test script to verify the RAG system is working correctly
"""

import sys
from pathlib import Path

print("🧪 Testing Product RAG System...")
print("=" * 60)

# Test 1: Check dependencies
print("\n1️⃣  Checking dependencies...")
try:
    import streamlit
    print("   ✅ Streamlit installed")
except ImportError:
    print("   ❌ Streamlit not found")
    sys.exit(1)

try:
    import langgraph
    print("   ✅ LangGraph installed")
except ImportError:
    print("   ❌ LangGraph not found")
    sys.exit(1)

try:
    import chromadb
    print("   ✅ ChromaDB installed")
except ImportError:
    print("   ❌ ChromaDB not found")
    sys.exit(1)

try:
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    print("   ✅ LangChain OpenAI installed")
except ImportError:
    print("   ❌ LangChain OpenAI not found")
    sys.exit(1)

# Test 2: Check environment
print("\n2️⃣  Checking environment...")
try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    if os.getenv("OPENAI_API_KEY"):
        print("   ✅ OpenAI API key found")
    else:
        print("   ⚠️  OpenAI API key not found in .env")
        print("   📝 Copy .env.example to .env and add your key")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Error loading environment: {e}")
    sys.exit(1)

# Test 3: Check products file
print("\n3️⃣  Checking products file...")
products_file = Path("products.txt")
if products_file.exists():
    print(f"   ✅ products.txt found")
    # Count products
    import json
    count = 0
    with open(products_file) as f:
        for line in f:
            line = line.rstrip(',\n').strip()
            if line:
                try:
                    json.loads(line)
                    count += 1
                except:
                    pass
    print(f"   📦 {count} products loaded")
else:
    print("   ❌ products.txt not found")
    sys.exit(1)

# Test 4: Initialize RAG system
print("\n4️⃣  Initializing RAG system...")
try:
    from product_rag import ProductRAG
    print("   ✅ ProductRAG imported successfully")
    
    print("   🔄 Creating ProductRAG instance...")
    rag = ProductRAG()
    print("   ✅ ProductRAG initialized successfully")
    print(f"   💾 Vector store ready with {len(rag.products_json)} products")
except Exception as e:
    print(f"   ❌ Error initializing RAG: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Run a test query
print("\n5️⃣  Running test query...")
try:
    test_query = "What products are good for athletes?"
    print(f"   ❓ Query: {test_query}")
    response = rag.query(test_query)
    print(f"   ✅ Response received ({len(response)} characters)")
    print(f"\n   📝 Response preview:")
    print(f"   {response[:200]}...")
except Exception as e:
    print(f"   ❌ Error running query: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ All tests passed! System is working correctly.")
print("\n🚀 You can now run: streamlit run app.py")
print("=" * 60)
