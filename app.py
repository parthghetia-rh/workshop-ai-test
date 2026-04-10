import os
from openai import OpenAI
import httpx
import warnings
# Suppress the ugly "InsecureRequestWarning" so the developers' output is clean
warnings.filterwarnings("ignore")

print("--- Initializing Client ---")

# We create a custom HTTP client that ignores the internal self-signed certificate (like curl -k)
custom_http_client = httpx.Client(verify=False)
import os
from openai import OpenAI
import httpx
import warnings

# Suppress the "InsecureRequestWarning" for the self-signed cluster certificate
warnings.filterwarnings("ignore")

print("--- Initializing Connection to OpenShift AI ---")

# Create a custom HTTP client that ignores the internal self-signed certificate
custom_http_client = httpx.Client(verify=False)

# The client automatically uses OPENAI_BASE_URL and OPENAI_API_KEY from the devfile
client = OpenAI(
    http_client=custom_http_client
)

# 1. DYNAMICALLY FETCH AND PRINT THE MODEL
try:
    # Query the vLLM server to see what model is currently loaded
    available_models = client.models.list()
    MODEL_NAME = available_models.data[0].id
    
    print(f"✅ Successfully connected to the internal cluster network!")
    print(f"🤖 Active GPU Model: {MODEL_NAME}")
except Exception as e:
    print(f"❌ Failed to connect to the model server. Check your Devfile URL.\nError: {e}")
    exit(1)

print("\n=======================================================")
print("💬 Welcome to the OpenShift AI Terminal Chatbot!")
print("Type 'exit' or 'quit' to end the conversation.")
print("=======================================================\n")

# 2. INITIALIZE CHAT HISTORY
# This acts as the "memory" for the chatbot
chat_history = [
    {"role": "system", "content": "You are a helpful, expert software engineering assistant. Keep your answers clear, accurate, and concise."}
]

# 3. THE CHATBOT LOOP
while True:
    # Get input from the developer
    user_input = input("You: ")
    
    # Check if the developer wants to quit
    if user_input.lower() in ['exit', 'quit']:
        print("Ending session. Goodbye!")
        break
        
    # Append the new user message to the history
    chat_history.append({"role": "user", "content": user_input})
    
    try:
        # Send the entire conversation history to the model
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=chat_history,
            max_tokens=500,
            temperature=0.7
        )
        
        # Extract the text response
        bot_reply = response.choices[0].message.content
        print(f"\nAI: {bot_reply}\n")
        
        # Append the AI's response to the history so it has context for the next turn
        chat_history.append({"role": "assistant", "content": bot_reply})
        
    except Exception as e:
        print(f"\n❌ Error generating response: {e}\n")