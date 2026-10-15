# ⚡ Groq AI Chatbot (Python)

A simple, fast, and responsive AI Chatbot powered by **Groq** and **Llama 3.3 / Llama 3.1**.

Includes both:
1. 💻 **Terminal CLI Chatbot** (`chatbot.py`) - Lightweight terminal interface with token-by-token streaming.
2. 🌐 **Web UI Chatbot** (`app.py`) - Sleek browser-based chat interface built with Streamlit.

---

## 🚀 Quick Setup

### 1. Add your Groq API Key
You can either:
- Create a `.env` file in this directory:
  ```env
  GROQ_API_KEY=your_groq_api_key_here
  ```
- Or simply run `python chatbot.py` and paste it when prompted (it will offer to save it for you!).

*(Get a free Groq API key at [console.groq.com/keys](https://console.groq.com/keys))*

---

## 💬 Running the Chatbot

### Option A: Terminal / CLI Mode
```bash
python chatbot.py
```

**Commands inside CLI chat:**
- `exit` or `quit` : Exit chat
- `clear` : Reset chat memory
- `models` : List available models
- `model <name>` : Switch model (e.g. `model llama-3.1-8b-instant`)
- `system <prompt>` : Set custom system prompt

---

### Option B: Web UI (Streamlit)
```bash
streamlit run app.py
```
This opens a modern ChatGPT-style web interface in your browser.

---

## 📦 Dependencies
Already installed on your system, but if needed elsewhere:
```bash
pip install -r requirements.txt
```
