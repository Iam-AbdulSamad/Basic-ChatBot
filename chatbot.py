import os
import sys
from dotenv import load_dotenv
from groq import Groq, AuthenticationError, APIConnectionError, RateLimitError

# Load environment variables from .env file if it exists
load_dotenv()

DEFAULT_MODEL = "llama-3.3-70b-versatile"
AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
    "openai/gpt-oss-120b"
]

def get_or_prompt_api_key() -> str:
    """Retrieve GROQ_API_KEY from environment or prompt the user."""
    api_key = os.getenv("GROQ_API_KEY")
    if api_key and api_key.strip() and not api_key.startswith("your_groq_api_key"):
        return api_key.strip()

    print("\n" + "="*50)
    print("  Groq API Key Not Found in Environment")
    print("="*50)
    print("Get your free API key at: https://console.groq.com/keys")
    user_key = input("Please enter your Groq API Key: ").strip()

    if not user_key:
        print("API key is required to start the chatbot. Exiting.")
        sys.exit(1)

    save_choice = input("Do you want to save this key to a .env file for future runs? (y/n): ").strip().lower()
    if save_choice in ("y", "yes"):
        try:
            with open(".env", "w", encoding="utf-8") as f:
                f.write(f"GROQ_API_KEY={user_key}\n")
            print("Successfully saved GROQ_API_KEY to .env file!\n")
        except Exception as e:
            print(f"Could not write to .env file: {e}")

    return user_key


def main():
    my_api_key = get_or_prompt_api_key()

    try:
        client = Groq(api_key=my_api_key)
    except Exception as e:
        print(f"Error initializing Groq client: {e}")
        sys.exit(1)

    current_model = DEFAULT_MODEL
    system_prompt = "You are a helpful, intelligent, and friendly AI assistant powered by Groq."
    
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    print("\n" + "="*60)
    print(f"  Groq AI Chatbot Ready!")
    print(f"  Model: {current_model}")
    print("="*60)
    print("Commands:")
    print("  'exit' or 'quit' : Exit chat")
    print("  'clear'          : Reset chat memory")
    print("  'model <name>'   : Switch model")
    print("  'models'         : List popular models")
    print("  'system <text>'  : Change system prompt")
    print("="*60 + "\n")

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        # Check for commands
        lower_input = user_input.lower().strip()
        if lower_input in ("exit", "quit", "q"):
            print("Goodbye! Have a great day!")
            break

        if lower_input == "clear":
            messages = [{"role": "system", "content": system_prompt}]
            print("[System] Chat memory cleared.")
            continue

        if lower_input == "models":
            print("\nPopular Groq Models:")
            for m in AVAILABLE_MODELS:
                marker = "*" if m == current_model else " "
                print(f"  [{marker}] {m}")
            continue

        if lower_input.startswith("model "):
            new_model = user_input.split(" ", 1)[1].strip()
            if new_model:
                current_model = new_model
                print(f"[System] Switched active model to: {current_model}")
            continue

        if lower_input.startswith("system "):
            new_sys = user_input.split(" ", 1)[1].strip()
            if new_sys:
                system_prompt = new_sys
                messages[0] = {"role": "system", "content": system_prompt}
                print(f"[System] System prompt updated to: \"{system_prompt}\"")
            continue

        # Append user message
        messages.append({"role": "user", "content": user_input})

        print("\nAI: ", end="", flush=True)

        try:
            stream = client.chat.completions.create(
                model=current_model,
                messages=messages,
                temperature=0.7,
                stream=True
            )

            full_reply = ""
            for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                full_reply += content

            print() # New line after streaming completes
            messages.append({"role": "assistant", "content": full_reply})

        except AuthenticationError:
            print("\n[Error] Invalid Groq API Key! Please verify your key at https://console.groq.com/keys")
            # Remove the last user message so the prompt doesn't get messed up
            messages.pop()
        except RateLimitError:
            print("\n[Error] Groq rate limit reached. Please wait a moment before sending another message.")
            messages.pop()
        except APIConnectionError:
            print("\n[Error] Could not connect to Groq API. Please check your internet connection.")
            messages.pop()
        except Exception as e:
            print(f"\n[Error] An unexpected error occurred: {e}")
            messages.pop()

if __name__ == "__main__":
    main()
