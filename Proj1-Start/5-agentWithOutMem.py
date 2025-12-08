from litellm import completion
from typing import List, Dict

def generate_response(messages: List[Dict]) -> str:
    """Call local LLM via LiteLLM to get response"""
    try:
        response = completion(
            model="ollama/qwen2.5:14b",  
            messages=messages,
            max_tokens=1024,
            # api_base="http://localhost:11434"  
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


messages = [
    {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
    {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
]

response = generate_response(messages)
print(response)

# Second query without including the previous response
messages = [
    {"role": "user", "content": "Update the function to include documentation."}
]

response = generate_response(messages)
print(response)