import json

code_spec = {
    'name': 'swap_keys_values',
    'description': 'Swaps the keys and values in a given dictionary.',
    'params': {
        'd': 'A dictionary with unique values.'
    },
}

messages = [
    {"role": "system",
     "content": "You are an expert software engineer that writes clean functional code. You always document your functions."},
    {"role": "user", "content": f"Please implement: {json.dumps(code_spec)}"}
]

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


response = generate_response(messages)
print(response)

'''
Certainly! Below is a Python implementation of the `swap_keys_values` function, which swaps the keys and values in a given dictionary. The function assumes that all values in the input dictionary are unique.

```python
def swap_keys_values(d):
    """
    Swaps the keys and values in a given dictionary.
    
    Parameters:
        d (dict): A dictionary with unique values.
        
    Returns:
        dict: A new dictionary where the original keys become values, and the original values become keys.
        
    Raises:
        ValueError: If any value in the input dictionary is not hashable or if there are duplicate values.
    """
    # Check that all values are hashable
    for value in d.values():
        try:
            hash(value)
        except TypeError:
            raise ValueError("All values must be hashable.")
    
    # Create a new dictionary with swapped keys and values
    swapped_dict = {value: key for key, value in d.items()}

    return swapped_dict

# Example usage:
original_dict = {'a': 1, 'b': 2, 'c': 3}
swapped_dict = swap_keys_values(original_dict)
print(swapped_dict)  # Output should be {1: 'a', 2: 'b', 3: 'c'}
```

### Explanation:

- **Function Parameters**:
  - `d`: The input dictionary where keys and values are to be swapped.

- **Return Value**: A new dictionary with the original keys as values, and the original values as keys.

- **Exception Handling**:
  - Raises a `ValueError` if any of the dictionary's values are not hashable (i.e., cannot be used as dictionary keys). This is necessary because all items in a dictionary must have unique and hashable keys.

This function will work correctly for dictionaries with unique values but will raise an error if there are duplicate values, since you can't have duplicate keys in a Python dictionary.
'''