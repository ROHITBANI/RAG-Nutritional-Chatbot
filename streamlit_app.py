import streamlit as st
import json
import requests
import time
from app import generate_response

# Use an empty API key string. The canvas environment will handle the actual key.
API_KEY = ""
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"

# Set up the Streamlit page configuration
st.set_page_config(page_title="Nutri-Bot Chatbot", layout="centered")

# Custom CSS for a better UI experience
st.markdown("""
<style>
    .st-emotion-cache-18ni7ap.e1rdg3o31 {
        visibility: hidden;
    }
    .st-emotion-cache-l9bibf.e16fv1qc1 {
        visibility: hidden;
    }
    .st-emotion-cache-6q9sum.e1ldz31w0 {
        background-color: #f3f4f6;
        padding: 2rem;
    }
    .st-emotion-cache-1c7y2qn.e1rdg3o31 {
        visibility: hidden;
    }
    .st-emotion-cache-12fmwz.e1s1ewg20 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #1f2937;
    }
    .st-emotion-cache-1av54w6.e1f1d6gn0 {
        padding: 1rem;
        background-color: #f0fdf4;
        border-radius: 0.75rem;
    }
    .st-emotion-cache-1r6509o.e1f1d6gn0 {
        padding: 1rem;
        background-color: #d1fae5;
        border-radius: 0.75rem;
    }
    .st-emotion-cache-1ky54u4.e1f1d6gn0 {
        color: #1f2937;
    }
    .st-emotion-cache-1c7y2qn.e1f1d6gn0 {
        font-size: 1.125rem;
    }
</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Application Title and description
st.title("Nutri-Bot")
st.markdown("Your AI Nutritional Expert built with RAG")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm Nutri-Bot, your personal nutritional advisor. What can I help you with today?",
    })

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask about a food, recipe, or health topic..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("Thinking..."):
        # Create a history list for the generate_response function
        chat_history = [{"role": "user" if m['role'] == 'user' else 'model', "parts": [{"text": m['content']}]} for m in st.session_state.messages]
        
        # Get response from the imported function
        response = generate_response(prompt, chat_history)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
