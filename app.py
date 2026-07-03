import streamlit as st
import sys
import os

# Streamlit Cloud sqlite3 patch for ChromaDB
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

# Ensure the src folder is in path
sys.path.append(os.path.join(os.path.dirname(__file__)))

try:
    from src.rag_pipeline import RAGPipeline
except ImportError as e:
    st.error(f"ImportError while loading RAGPipeline: {e}")
    st.error("Ensure all dependencies are in requirements.txt and you are running from the project root.")
    st.stop()

st.set_page_config(page_title="Mutual Fund FAQ Assistant", page_icon="📈", layout="centered")

st.title("Mutual Fund FAQ Assistant")
st.markdown("### ⚠️ Disclaimer: Facts-only. No investment advice.")

if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # Add a welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I can provide factual information about HDFC Mutual Funds based on official documents. How can I help you today?"
    })

# Define example questions
example_questions = [
    "What is the exit load for HDFC Small Cap Fund?",
    "What is the riskometer classification for HDFC ELSS Tax Saver?",
    "What is the expense ratio of HDFC Liquid Fund?"
]

st.markdown("**Example Questions:**")
cols = st.columns(3)
for i, col in enumerate(cols):
    if col.button(example_questions[i], key=f"btn_{i}"):
        st.session_state.preset_question = example_questions[i]

@st.cache_resource
def load_pipeline():
    try:
        return RAGPipeline()
    except Exception as e:
        st.error(f"Failed to load RAG Pipeline (Check API Keys & ChromaDB): {e}")
        return None

pipeline = load_pipeline()

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Check for preset question from buttons
user_input = st.chat_input("Ask a question about a mutual fund...")
if "preset_question" in st.session_state:
    user_input = st.session_state.preset_question
    del st.session_state.preset_question

if user_input:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Searching official documents..."):
            if pipeline:
                response = pipeline.process_query(user_input)
            else:
                response = "The system is not properly initialized. Please check your API keys and ensure data has been indexed."
            st.markdown(response)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
