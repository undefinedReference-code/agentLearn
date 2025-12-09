import re
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
    

def extract_specific_code_blocks(text: str, language: str = "python") -> List[str]:

    pattern = rf"```{language}\s*\n(.*?)```"
    
    code_blocks = re.findall(pattern, text, re.DOTALL)
    
    cleaned_blocks = []
    for block in code_blocks:
        cleaned = block.strip()
        if cleaned:
            cleaned_blocks.append(cleaned)
    
    return cleaned_blocks


if __name__ == "__main__" :
    # userInput = input("what function do you want to create: ")

    userInput = "calculate the n-th of Fibonacci sequence" # mock

    systemPrompt = "You are an expert Python software engineer who prefers functional programming. When providing Python code, adhere to these strict requirements:\n " \
    "1. Write all Python code exclusively within ```python ``` code blocks. " \

    messages = [
        {"role": "system", "content": systemPrompt},
        {"role": "user", "content": f"Write a function to satisfy the need of user {userInput}."}
    ]
    
    response = generate_response(messages=messages)

    print(response)

    print("extract code")

    cleaned_blocks = extract_specific_code_blocks(response)
    print(f"first prompt find {len(cleaned_blocks)} codes:")
    print(cleaned_blocks)

    if len(cleaned_blocks) > 1 :
        systemPrompt = f"You are an expert Python performance analyst. Given multiple Python code blocks that implement the same functionality, analyze them carefully to select the most efficient one in terms of execution speed and memory usage.\n" \
        "When providing your analysis, first explain your reasoning about each code block's time and space complexity, then output ONLY the selected code block wrapped in pythontags. Do not include any usage examples, test cases, or other code outside the function definition.\n "\
        "In your analysis, consider:\n" \
        "1. Time complexity (Big O notation)\n" \
        "2. Space complexity (memory usage)\n" \
        "3. Algorithm efficiency\n" \
        "4. Use of efficient data structures and patterns\n" \
        "5. Potential bottlenecks or inefficiencies\n" \
        "6. Functional correctness and adherence to the user's requirement {userInput} is the primary criterion. Only consider code blocks that correctly implement the requested functionality. If a code block does not implement the required function, discard it"

        content = ""
        for code in cleaned_blocks: 
            content += "```python\n"
            content += code
            content += "\n```"
        
        messages = [
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": content}
        ]

        response = generate_response(messages)

        print(response)

        targetCode = extract_specific_code_blocks(response)[0]
    else:
        targetCode = cleaned_blocks[0]

    print("final targets: ")
    print(targetCode)