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

"""
Certainly! Swapping the keys and values of a dictionary involves creating a new dictionary where what were originally the values become the keys, and the original keys become the values. However, you should be careful with this operation because multiple keys might map to the same value, which could cause collisions (multiple keys would end up mapping to one key in the swapped dictionary). To handle this, we can use lists as values for keys that are mapped by several other keys.

Here is a Python function using functional programming principles:

```python
from typing import Dict, Any

def swap_dict_keys_values(d: Dict[Any, Any]) -> Dict[Any, list]:
    # Initialize an empty dictionary to hold the swapped key-value pairs.
    swapped_dict = {}

    for original_key, original_value in d.items():
        if original_value not in swapped_dict:
            swapped_dict[original_value] = [original_key]
        else:
            swapped_dict[original_value].append(original_key)

    return swapped_dict
```

### Explanation:
- **Initialization**: `swapped_dict` starts as an empty dictionary.
- **Iteration**: For each key-value pair `(original_key, original_value)` in the input dictionary `d`, we check if `original_value` is already a key in `swapped_dict`.
  - If not: We add it to `swapped_dict` with its value being `[original_key]`.
  - If yes: We append `original_key` to the existing list.
- **Return**: The function returns the newly created dictionary where original values are keys and original keys are lists of values that mapped to those keys.

### Example:
Given a dictionary like `{ 'a': 1, 'b': 2, 'c': 1 }`, this function will return `{ 1: ['a', 'c'], 2: ['b'] }`.

This approach ensures that no information is lost due to key collisions in the output dictionary.
"""

# Second query without including the previous response
messages = [
    {"role": "user", "content": "Update the function to include documentation."}
]

response = generate_response(messages)
print(response)

"""
Sure! Could you please provide me with the function that needs to be documented? Without seeing the code, I won't be able to add proper documentation comments. Please share the details of the function or at least its purpose and parameters.
"""

