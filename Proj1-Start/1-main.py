
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

print("Sending request to local Qwen model...")
response = generate_response(messages)
print("Response received:")
print(response)


""" example output
Sending request to local Qwen model...
Response received:
Certainly! Swapping the keys and values of a dictionary can be done using Python with a functional approach. However, it's important to note that if your original dictionary has duplicate values, only one key-value pair will be preserved when swapping them because dictionaries cannot have duplicate keys. Here’s how you could implement this:

```python
from typing import Dict, Any

def swap_keys_values(d: Dict[Any, Any]) -> Dict[Any, Any]:
    # Using dict comprehension to create a new dictionary with swapped keys and values
    return {v: k for k, v in d.items()}

# Example usage:
original_dict = {'a': 1, 'b': 2, 'c': 3}
swapped_dict = swap_keys_values(original_dict)
print(swapped_dict)  # Output will be {1: 'a', 2: 'b', 3: 'c'}
```

In this function:
- `d.items()` generates a view of the dictionary’s key-value pairs.
- `{v: k for k, v in d.items()}` creates a new dictionary by iterating over each item and swapping keys with values. If there are duplicate values, only the last occurrence will be stored.

This solution leverages Python's functional programming capabilities through dict comprehension to achieve the desired result efficiently.
"""