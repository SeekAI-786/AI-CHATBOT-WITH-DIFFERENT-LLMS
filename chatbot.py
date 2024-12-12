import streamlit as st
from huggingface_hub import InferenceClient
import requests
import json
import pdfplumber  # For extracting text from PDFs

# Hardcoded API keys (Replace with actual keys)
HF_API_KEY = "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"  # For Hugging Face API integration

# Initialize session state for storing conversations and PDF content
if "conversations" not in st.session_state:
    st.session_state.conversations = []
if "pdf_content" not in st.session_state:
    st.session_state.pdf_content = ""

# App Title and Layout
st.title("Medi Bot 🤖💬")
st.caption("Your personalized medical assistant powered by GPT. Created by Qusai Jamali (22108131) and Muhammad (22108137)")

# Model Selection
st.sidebar.subheader("Model Selection")
available_models = [
    "gemma-mental-health-fine-tune",
    "qwen-1.5B-medical-QA",
    "llama-3.2-1B-Lora-Fine_Tune-FineTome"
]
selected_model = st.sidebar.selectbox("Choose a model:", available_models)

# User Input Section at the bottom
st.subheader("💬 Chat with the Medi Bot")
user_query = st.text_input("Your message:", placeholder="Type your query here...")

# Buttons for response generation and clearing
col1, col2 = st.columns([1, 0.320])
with col1:
    generate_button = st.button("Generate Response")
with col2:
    clear_button = st.button("Clear Conversation History")

# Handle Clear Button
if clear_button:
    st.session_state.conversations = []
    st.session_state.pdf_content = ""
    st.success("Conversation history and PDF content cleared.")

# Handle Generate Button
if generate_button:
    if not user_query.strip():
        st.warning("Please enter a message.")
    else:
        # Generate Response based on model selection
        response = None

        # User-friendly bot instruction to refrain from personal or abusive answers
        friendly_instruction = (
            "You are a helpful and friendly medical assistant. Please refrain from giving personal, offensive, "
            "or abusive answers. Be respectful and professional in your responses."
        )

        # Hugging Face API for Yi Chat, Llama, and Phi models
        try:
            client = InferenceClient(api_key=HF_API_KEY)
            messages = [{"role": "system", "content": friendly_instruction}, {"role": "user", "content": user_query}]

            # Handle model-specific conditions
            if selected_model == "qwen-1.5B-medical-QA":
                model_name = "Yi-1.5-34B-Chat"  # Update model name for this selection

            elif selected_model == "llama-3.2-1B-Lora-Fine_Tune-FineTome":
                model_name = "meta-llama/Llama-3.2-1B-Instruct"  # Update model name for this selection

            elif selected_model == "gemma-mental-health-fine-tune":
                model_name = "google/gemma-1.1-2b-it"  # Update model name for this selection

            # Call Hugging Face API with the selected model
            completion = client.chat.completions.create(
                model=model_name, messages=messages, max_tokens=700
            )
            response = completion.choices[0].message.content
        except Exception as e:
            st.error(f"Hugging Face API error: {e}")

        # Display the response below the input field
        if response:
            st.session_state.conversations.append({"query": user_query, "response": response})
            st.success("Response generated!")
            st.write(f"**Response:** {response}")

# Display previous conversation history
if st.session_state.conversations:
    st.subheader("📝 Previous Conversations")
    # Reverse the list so that the latest conversation is shown at the top
    for idx, convo in enumerate(reversed(st.session_state.conversations)):
        st.write(f"**Prompt {len(st.session_state.conversations) - idx}:** {convo['query']}")
        st.write(f"**Response {len(st.session_state.conversations) - idx}:** {convo['response']}")
