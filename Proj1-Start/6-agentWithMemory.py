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
Swapping keys and values in a dictionary can be tricky because dictionaries require unique keys, so if there are duplicate values in the original dictionary, we need to handle them appropriately. One way to handle this is by making the values into lists of their corresponding keys (since multiple keys could map to the same value).

Here's an example function that performs this operation:

```python
def swap_dict_keys_values(original_dict):
    # Initialize a new dictionary with list values
    swapped_dict = {}

    for key, value in original_dict.items():
        if value not in swapped_dict:
            # If the value is not already in the dictionary, add it as a new entry
            swapped_dict[value] = [key]
        else:
            # Append the key to the list of keys that map to this value
            swapped_dict[value].append(key)

    return swapped_dict

# Example usage
original_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 1}
swapped_dict = swap_dict_keys_values(original_dict)

print(swapped_dict)  # Output: {1: ['a', 'd'], 2: ['b'], 3: ['c']}
```

This function will create a new dictionary where each value from the original dictionary is now a key, and its associated keys are stored in a list. If there were no duplicate values in the original dictionary, each entry would have just one element in the list.

If you want to handle cases where multiple keys map to unique values more elegantly (without lists), it might be best to consider why you're swapping keys with potentially non-unique values and whether another data structure or approach is needed. But for a direct swap preserving all information, this solution works well
"""

# We are going to make this verbose so it is clear what
# is going on. In a real application, you would likely
# just append to the messages list.
messages = [
   {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
   {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."},
   
   # Here is the assistant's response from the previous step
   # with the code. This gives it "memory" of the previous
   # interaction.
   {"role": "assistant", "content": response},
   
   # Now, we can ask the assistant to update the function
   {"role": "user", "content": "Update the function to include documentation."}
]

response = generate_response(messages)
print(response)

'''
Certainly! Here's the updated function with detailed docstrings:

```python
def swap_dict_keys_values(original_dict):
    """
    Swaps keys and values in a dictionary where each key maps to exactly one value.

    Parameters:
        original_dict (dict): The input dictionary whose keys are to be swapped with their corresponding values.

    Returns:
        dict: A new dictionary where the keys of `original_dict` have become values, and vice versa. If multiple
              keys in the input map to the same value, those keys will be aggregated into a list for that value.

    Example usage:
        >>> original_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 1}
        >>> swapped_dict = swap_dict_keys_values(original_dict)
        >>> print(swapped_dict)
        {1: ['a', 'd'], 2: ['b'], 3: ['c']}
    """

    # Initialize a new dictionary with list values
    swapped_dict = {}

    for key, value in original_dict.items():
        if value not in swapped_dict:
            # If the value is not already in the dictionary, add it as a new entry
            swapped_dict[value] = [key]
        else:
            # Append the key to the list of keys that map to this value
            swapped_dict[value].append(key)

    return swapped_dict

# Example usage
original_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 1}
swapped_dict = swap_dict_keys_values(original_dict)

print(swapped_dict)  # Output: {1: ['a', 'd'], 2: ['b'], 3: ['c']}
```

This function now includes a comprehensive docstring that describes the parameters, return value, and provides an example usage. The docstring helps users understand how to use the function correctly and what they should expect as output.
'''