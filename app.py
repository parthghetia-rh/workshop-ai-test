import os
from openai import OpenAI

# Initialize the client. It automatically picks up the internal 
# OpenShift AI environment variables from your devfile!
client = OpenAI()

# Make sure this matches the exact name you gave the model when 
# you deployed it in the OpenShift AI UI (e.g., granite-8b-code-instruct)
MODEL_NAME = "granite-8b-code-instruct"

def run_basic_prompt():
    print(f"--- Sending request to local {MODEL_NAME} on OpenShift AI ---")
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful, senior software engineer mentoring a junior developer."},
                {"role": "user", "content": "Explain what a REST API is in two simple sentences."}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        print("\nResponse from Model:")
        print(response.choices[0].message.content)
        print("\n---------------------------------------------------------")
        
    except Exception as e:
        print(f"Error connecting to the model: {e}")
        print("Check your OPENAI_API_BASE environment variable.")

if __name__ == "__main__":
    run_basic_prompt()