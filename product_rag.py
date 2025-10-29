"""
Product RAG System with LangGraph
Implements a RAG (Retrieval-Augmented Generation) system for grocery products
using LangGraph state machines and OpenAI embeddings.
"""

import json
import os
import sys
import warnings
from pathlib import Path
from typing import List, Dict, Annotated, TypedDict, Literal
from operator import add

# Suppress warnings before any imports
warnings.filterwarnings('ignore')
os.environ['ANONYMIZED_TELEMETRY'] = 'False'

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
load_dotenv()

# Suppress ChromaDB logging
import logging
logging.getLogger('chromadb').setLevel(logging.ERROR)

# Import chromadb after setting environment variable
import chromadb

# Monkey patch to suppress telemetry errors
def silent_capture(*args, **kwargs):
    pass

try:
    if hasattr(chromadb.telemetry.product.posthog, 'Posthog'):
        chromadb.telemetry.product.posthog.Posthog.capture = silent_capture
except:
    pass


class Product(BaseModel):
    """Product model representing a grocery item"""
    id: str = Field(..., description="Unique identifier (SKU) for the product")
    name: str = Field(..., description="Name of the product")
    description: str = Field(default="", description="Product description")
    brandName: str = Field(default="", description="Brand name")
    price: Dict = Field(default_factory=dict, description="Price information")
    categories: List[Dict] = Field(default_factory=list, description="Product categories")


class AgentState(TypedDict):
    """State of the RAG agent"""
    messages: Annotated[List, add]
    query: str
    context: str
    products: List[Dict]


class ProductRAG:
    """
    RAG system for product search using LangGraph.
    Manages vector database, embeddings, and conversational search.
    """
    
    def __init__(self, products_file: str = "products.txt"):
        """Initialize the RAG system"""
        self.products_file = Path(__file__).parent / products_file
        self.chroma_dir = Path(__file__).parent / "chroma_db_openai"
        
        # Initialize OpenAI components
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Load products
        self.products_json = self._load_products()
        
        # Initialize or load vector store
        self.vector_store = self._init_vector_store()
        
        # Create LangGraph workflow
        self.graph = self._create_graph()
        
    def _load_products(self) -> List[Dict]:
        """Load products from JSON file"""
        products = []
        with open(self.products_file, 'r') as file:
            for line in file:
                line = line.rstrip(',\n')
                try:
                    product = json.loads(line.strip())
                    products.append(product)
                except json.JSONDecodeError as e:
                    print(f"Error parsing line: {line}\n{e}")
        return products
    
    def _init_vector_store(self) -> Chroma:
        """Initialize or load the Chroma vector store"""
        # Check if vector store already exists
        if self.chroma_dir.exists() and any(self.chroma_dir.iterdir()):
            print("Loading existing vector store...")
            return Chroma(
                persist_directory=str(self.chroma_dir),
                embedding_function=self.embeddings
            )
        
        print("Creating new vector store with OpenAI embeddings...")
        
        # Prepare documents for embedding
        documents = []
        metadatas = []
        
        for product in self.products_json:
            # Create rich text representation for better search
            text = f"""
            Product: {product.get('name', '')}
            Brand: {product.get('brandName', '')}
            Description: {product.get('description', '')}
            Categories: {', '.join([cat.get('name', '') for cat in product.get('categories', [])])}
            Price: ${product.get('price', {}).get('amount', 0) / 100:.2f}
            """
            
            documents.append(text)
            # Filter out None values from metadata to avoid ChromaDB errors
            metadata = {
                'id': product.get('sku') or 'unknown',
                'name': product.get('name') or 'Unknown Product',
                'brandName': product.get('brandName') or 'Unknown Brand',
            }
            metadatas.append(metadata)
        
        # Create vector store (telemetry disabled via environment variable)
        vector_store = Chroma.from_texts(
            texts=documents,
            embedding=self.embeddings,
            metadatas=metadatas,
            persist_directory=str(self.chroma_dir)
        )
        
        print(f"Vector store created with {len(documents)} products")
        return vector_store
    
    def get_product_by_sku(self, sku: str) -> Dict:
        """Get product details by SKU"""
        for product in self.products_json:
            if product.get('sku') == sku:
                return product
        return {}
    
    def _create_tools(self):
        """Create tools for the agent"""
        
        @tool
        def search_products(query: str, limit: int = 5) -> str:
            """
            Search for products based on a query.
            Returns detailed product information including name, brand, price, and description.
            """
            results = self.vector_store.similarity_search_with_score(query, k=limit)
            
            products_info = []
            for doc, score in results:
                sku = doc.metadata.get('id')
                product = self.get_product_by_sku(sku)
                
                if product:
                    price_info = product.get('price', {})
                    price = price_info.get('amountRelevantDisplay', 'N/A')
                    
                    products_info.append({
                        'name': product.get('name', 'Unknown'),
                        'brand': product.get('brandName', 'Unknown'),
                        'price': price,
                        'description': product.get('description', '')[:200],
                        'relevance_score': f"{1 - score:.2f}"
                    })
            
            return json.dumps(products_info, indent=2)
        
        @tool
        def get_products_by_category(category_name: str) -> str:
            """
            Get products filtered by category name (e.g., 'Snacks', 'Dairy & Eggs', 'Frozen Foods').
            """
            matching_products = []
            
            for product in self.products_json:
                categories = product.get('categories', [])
                for cat in categories:
                    if category_name.lower() in cat.get('name', '').lower():
                        price_info = product.get('price', {})
                        matching_products.append({
                            'name': product.get('name'),
                            'brand': product.get('brandName'),
                            'price': price_info.get('amountRelevantDisplay', 'N/A'),
                        })
                        break
            
            return json.dumps(matching_products[:10], indent=2)
        
        @tool
        def suggest_products_for_recipe(recipe_type: str) -> str:
            """
            Suggest products suitable for a specific recipe type.
            Examples: 'pasta', 'salad', 'breakfast', 'dessert', 'soup'
            """
            query = f"ingredients for {recipe_type} recipe cooking"
            results = self.vector_store.similarity_search(query, k=8)
            
            suggestions = []
            for doc in results:
                sku = doc.metadata.get('id')
                product = self.get_product_by_sku(sku)
                if product:
                    suggestions.append({
                        'name': product.get('name'),
                        'brand': product.get('brandName'),
                        'price': product.get('price', {}).get('amountRelevantDisplay', 'N/A')
                    })
            
            return json.dumps(suggestions, indent=2)
        
        @tool
        def find_products_for_athletes() -> str:
            """
            Find products suitable for athletes - high protein, healthy options.
            """
            queries = [
                "high protein lean meat chicken turkey fish",
                "greek yogurt protein",
                "organic healthy vegetables",
            ]
            
            all_products = []
            for query in queries:
                results = self.vector_store.similarity_search(query, k=3)
                for doc in results:
                    sku = doc.metadata.get('id')
                    product = self.get_product_by_sku(sku)
                    if product and product not in all_products:
                        all_products.append({
                            'name': product.get('name'),
                            'brand': product.get('brandName'),
                            'price': product.get('price', {}).get('amountRelevantDisplay', 'N/A'),
                            'description': product.get('description', '')[:150]
                        })
            
            return json.dumps(all_products[:10], indent=2)
        
        return [search_products, get_products_by_category, suggest_products_for_recipe, find_products_for_athletes]
    
    def _create_graph(self):
        """Create the LangGraph workflow"""
        tools = self._create_tools()
        llm_with_tools = self.llm.bind_tools(tools)
        
        # Define the agent node
        def agent(state: AgentState):
            """Agent node that decides what to do"""
            messages = state["messages"]
            response = llm_with_tools.invoke(messages)
            return {"messages": [response]}
        
        # Define routing logic
        def should_continue(state: AgentState) -> Literal["tools", "end"]:
            """Determine if we should continue or end"""
            messages = state["messages"]
            last_message = messages[-1]
            
            # If there are no tool calls, end
            if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
                return "end"
            return "tools"
        
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", agent)
        workflow.add_node("tools", ToolNode(tools))
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "tools": "tools",
                "end": END
            }
        )
        
        # Add edge from tools back to agent
        workflow.add_edge("tools", "agent")
        
        # Compile with memory
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)
    
    def query(self, question: str, thread_id: str = "default") -> str:
        """
        Query the RAG system with a question.
        
        Args:
            question: User's question
            thread_id: Thread ID for conversation history
            
        Returns:
            AI response as a string
        """
        system_message = SystemMessage(content="""You are a helpful grocery store assistant. 
        You help customers find products, suggest items for recipes, and provide information about grocery items.
        Use the available tools to search for products and provide detailed, helpful recommendations.
        Always be friendly and informative.""")
        
        # Create initial state
        initial_state = {
            "messages": [system_message, HumanMessage(content=question)],
            "query": question,
            "context": "",
            "products": []
        }
        
        # Run the graph
        config = {"configurable": {"thread_id": thread_id}}
        
        result = self.graph.invoke(initial_state, config)
        
        # Extract the final response
        final_message = result["messages"][-1]
        return final_message.content


if __name__ == "__main__":
    # Test the RAG system
    rag = ProductRAG()
    
    print("\n=== Testing Product RAG System ===\n")
    
    # Test queries
    test_queries = [
        "What products are good for athletes?",
        "Suggest some products for a pasta recipe",
        "Show me some dairy products",
        "What snacks do you have?",
    ]
    
    for query in test_queries:
        print(f"\nQ: {query}")
        response = rag.query(query)
        print(f"A: {response}\n")
        print("-" * 80)
