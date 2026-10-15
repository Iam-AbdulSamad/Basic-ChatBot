import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq, AuthenticationError, APIConnectionError, RateLimitError

# Page setup
st.set_page_config(
    page_title="Groq AI Chatbot",
    page_icon="⚡",
    layout="centered"
)

# Load existing environment variables
load_dotenv()

# Sidebar: Configuration
with st.sidebar:
    st.title("⚡ Groq Settings")
    
    # API Key Input
    saved_api_key = os.getenv("GROQ_API_KEY", "")
    api_key = st.text_input(
        "Groq API Key",
        value=saved_api_key,
        type="password",
        placeholder="gsk_...",
        help="Get your key at https://console.groq.com/keys"
    )
    
    # Model Selection
    model = st.selectbox(
        "Choose Model",
        options=[
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
            "openai/gpt-oss-120b"
        ],
        index=0
    )
    
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.5, value=0.7, step=0.1)
    
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful, intelligent, and friendly AI assistant powered by Groq.",
        height=100
    )
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

st.title("⚡ Groq AI Chatbot")
st.caption("Powered by Groq's ultra-fast LPU inference engine")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User prompt input
if prompt := st.chat_input("Ask anything..."):
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar to chat.")
        st.stop()

    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            client = Groq(api_key=api_key)
            
            # Prepare messages payload including system prompt
            api_messages = [{"role": "system", "content": system_prompt}]
            api_messages.extend([
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ])

            response_stream = client.chat.completions.create(
                model=model,
                messages=api_messages,
                temperature=temperature,
                stream=True,
            )

            for chunk in response_stream:
                chunk_text = chunk.choices[0].delta.content or ""
                full_response += chunk_text
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except AuthenticationError:
            st.error("Authentication Error: Invalid Groq API Key.")
        except RateLimitError:
            st.warning("Rate limit reached. Please wait a moment before sending another message.")
        except APIConnectionError:
            st.error("Connection Error: Unable to reach Groq API. Check your internet connection.")
        except Exception as e:
            st.error(f"Error: {e}")
