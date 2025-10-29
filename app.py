"""
Streamlit Chatbot Interface for Product RAG System
Interactive grocery store assistant powered by LangGraph and OpenAI
"""

import os
import warnings
import sys

# Suppress warnings and telemetry before any imports
warnings.filterwarnings('ignore')
os.environ['ANONYMIZED_TELEMETRY'] = 'False'

# Redirect stderr to suppress telemetry messages
import io
from contextlib import redirect_stderr

import streamlit as st
from product_rag import ProductRAG
import uuid


# Page configuration
st.set_page_config(
    page_title="Grocery Store Assistant",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
    
    if "rag_system" not in st.session_state:
        # Check if this is first run (vector DB doesn't exist)
        import os
        is_first_run = not os.path.exists("chroma_db_openai")
        
        if is_first_run:
            # Show detailed first-run message
            init_placeholder = st.empty()
            with init_placeholder.container():
                st.info("🚀 **First-Time Setup in Progress**")
                st.markdown("""
                This is the first time running the app. We're setting up:
                
                1. 📚 Loading 4,574 grocery products from database
                2. 🧠 Creating AI embeddings using OpenAI
                3. 💾 Building vector search index with ChromaDB
                
                **This takes 2-3 minutes and only happens once.**
                
                Future app starts will be instant! ⚡
                """)
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate progress updates (actual creation happens in ProductRAG)
                import time
                for i in range(3):
                    if i == 0:
                        status_text.text("📚 Loading product data...")
                        progress_bar.progress(10)
                    elif i == 1:
                        status_text.text("🧠 Creating embeddings (this is the slow part)...")
                        progress_bar.progress(30)
                    elif i == 2:
                        status_text.text("💾 Building search index...")
                        progress_bar.progress(50)
                    time.sleep(0.5)
                
                progress_bar.progress(60)
                status_text.text("🔧 Finalizing setup...")
            
            with st.spinner("Creating vector database (please wait 2-3 minutes)..."):
                try:
                    # Suppress stderr during initialization to hide ChromaDB warnings
                    with redirect_stderr(io.StringIO()):
                        st.session_state.rag_system = ProductRAG()
                    
                    # Clear initialization message and show success
                    init_placeholder.empty()
                    st.success("✅ **Setup Complete!** The app is now ready to use. Future visits will be instant!")
                    time.sleep(2)  # Show success message briefly
                    st.rerun()  # Refresh to clear success message
                    
                except Exception as e:
                    init_placeholder.empty()
                    st.error(f"❌ **Setup Failed:** {str(e)}")
                    st.info("Please check your OpenAI API key in the secrets settings.")
                    st.stop()
        else:
            # Quick load on subsequent runs
            with st.spinner("🔄 Loading RAG system..."):
                try:
                    # Suppress stderr during initialization to hide ChromaDB warnings
                    with redirect_stderr(io.StringIO()):
                        st.session_state.rag_system = ProductRAG()
                except Exception as e:
                    st.error(f"❌ Failed to load system: {str(e)}")
                    st.stop()


def display_chat_message(role: str, content: str):
    """Display a chat message with appropriate styling"""
    with st.chat_message(role):
        st.markdown(content)


def main():
    """Main Streamlit application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("Grocery Assistant")
        st.markdown("---")
        
        st.markdown("""
        ### Welcome! 
        
        I'm your AI-powered grocery store assistant. I can help you with:
        
        - **Product Search** - Find specific items
        - **Athletic Nutrition** - Products for athletes
        - **Recipe Suggestions** - Ingredients for your meals
        - **Category Browsing** - Explore product categories
        - **Price Information** - Compare prices
        
        ### Example Questions:
        - "What products are good for athletes?"
        - "Suggest ingredients for a pasta recipe"
        - "Show me dairy products"
        - "What healthy snacks do you have?"
        - "Find me some frozen vegetables"
        """)
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.rerun()
        
        # System info
        with st.expander("ℹSystem Information"):
            st.info(f"""
            **Thread ID:** `{st.session_state.thread_id[:8]}...`
            
            **Model:** GPT-4o-mini
            
            **Embeddings:** text-embedding-3-small
            
            **Products Loaded:** {len(st.session_state.rag_system.products_json)}
            """)
    
    # Main chat interface
    st.title("🛒 Grocery Store Assistant Chat")
    st.markdown("Ask me anything about our products!")
    
    # Display chat history
    for message in st.session_state.messages:
        display_chat_message(message["role"], message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about products, recipes, or get recommendations..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.rag_system.query(
                        prompt,
                        thread_id=st.session_state.thread_id
                    )
                    
                    st.markdown(response)
                    
                    # Add assistant response to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
    
    # Quick action buttons
    if len(st.session_state.messages) == 0:
        st.markdown("### 💡 Quick Start Questions:")
        
        col1, col2, col3 = st.columns(3)
        
        button_prompt = None
        
        with col1:
            if st.button("Athletic Products", use_container_width=True):
                button_prompt = "What products are good for athletes?"
        
        with col2:
            if st.button("🍝 Pasta Recipe", use_container_width=True):
                button_prompt = "Suggest ingredients for a pasta recipe"
        
        with col3:
            if st.button("🥗 Healthy Snacks", use_container_width=True):
                button_prompt = "Show me healthy snacks"
        
        # Process button click
        if button_prompt:
            st.session_state.messages.append({"role": "user", "content": button_prompt})
            display_chat_message("user", button_prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.rag_system.query(
                            button_prompt,
                            thread_id=st.session_state.thread_id
                        )
                        
                        st.markdown(response)
                        
                        # Add assistant response to history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response
                        })
                        
                    except Exception as e:
                        error_msg = f"Sorry, I encountered an error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_msg
                        })
            
            st.rerun()


if __name__ == "__main__":
    main()
