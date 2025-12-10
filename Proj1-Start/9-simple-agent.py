import json
import re
from litellm import completion
from typing import List, Dict
import sys

def extract_markdown_block(text: str, language: str = "python") -> List[str]:

    pattern = rf"```{language}\s*\n(.*?)```"
    
    code_blocks = re.findall(pattern, text, re.DOTALL)
    
    cleaned_blocks = [block.strip() for block in code_blocks if block.strip()]
    
    return cleaned_blocks


def parse_action(response: str) -> Dict:
    """Parse the LLM response into a structured action dictionary."""
    try:
        response = extract_markdown_block(response, "action")[0]
        response_json = json.loads(response)
        if "tool_name" in response_json and "args" in response_json:
            return response_json
        else:
            return {"tool_name": "error", "args": {"message": "You must respond with a JSON tool invocation."}}
    except json.JSONDecodeError:
        return {"tool_name": "error", "args": {"message": "Invalid JSON response. You must respond with a JSON tool invocation."}}


def generate_response(messages: List[Dict]) -> str:
   """Call LLM to get response"""
   response = completion(
      model="ollama/qwen2.5:14b",
      messages=messages,
      max_tokens=1024
   )
   return response.choices[0].message.content

agent_rules = [{
    "role": "system",
    "content":  """
                You are an AI agent that can perform tasks by using available tools.

                Available tools:
                - list_files() -> List[str]: List all files in  current directory
                - read_file(file_name: str) -> str: Read the content of a file.
                - terminate(message: str): End the agent loop and print a summary to the user.

                If a user asks about files, list them before reading.

                Every response MUST have an action.
                Respond in this format:

                ```action
                {
                    "tool_name": "insert tool_name",
                    "args": {...fill in any required arguments here...}
                }
                ```
                After you have successfully listed the files AND read the content of the specific file the user is interested in, your task is complete. You should then use the 'terminate' tool to end the conversation with a summary. You final output it the args of 'terminate'
                """
}]
'''
- Role of system messages: The system role in the messages list is used to establish ground rules for the agent. This ensures the LLM understands what it can do and how it should behave throughout the session.
- Tools description: The agent rules explicitly list the tools the agent can use, providing a structured interface for interaction with the environment.
- Output format: The rules enforce a standardized output format ("```action {...}"), which makes parsing and executing actions easier and less error-prone.

Each of the “tools” in the system prompt correspond to a function in the code. The agent is going to choose what function to execute and when. Moreover, it is going to decide the parameters that are provided to the functions.
'''

import os
from typing import List

def list_files(directory: str = ".") -> List[str]:
    try:
        if not os.path.exists(directory):
            return {"error": f"Directory '{directory}' does not exist"}
        
        items = os.listdir(directory)
        
        files = [item for item in items if os.path.isfile(os.path.join(directory, item))]
        
        return {"result": files}
        
    except PermissionError:
        return {"error": f"Permission denied to access directory '{directory}'"}
    except Exception as e:
        return {"error": f"Error listing files: {str(e)}"}
    

def read_file(file_name: str) -> str:
    try:
        if not os.path.exists(file_name):
            current_dir_file = os.path.join(".", file_name)
            if not os.path.exists(current_dir_file):
                return {"error": f"File '{file_name}' does not exist"}
            file_name = current_dir_file
        
        if not os.path.isfile(file_name):
            return {"error": f"'{file_name}' is not a file"}
        
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
            
        return {"result": content}
        
    except PermissionError:
        return {"error": f"Permission denied to read file '{file_name}'"}
    except UnicodeDecodeError:
        try:
            with open(file_name, 'r', encoding='latin-1') as file:
                content = file.read()
            return {"result": content}
        except Exception as e:
            return {"error": f"Error reading file (encoding issue): {str(e)}"}
    except Exception as e:
        return {"error": f"Error reading file: {str(e)}"}


if __name__ == "__main__" :
    
    iterations = 0
    memory = []
    max_iterations = 20
    userPromt = input("input what you want to do\n")

    memory.extend([
        {"role": "user", "content": userPromt}
    ])
    # The Agent Loop
    while iterations < max_iterations:


        # 1. Construct prompt: Combine agent rules with memory
        prompt = agent_rules + memory

        '''
        Explanation:
            - agent_rules: This contains the predefined system instructions, ensuring the agent behaves within its defined constraints and understands its tools.
            - memory: This is a record of all past interactions, including user input, the agent's responses, and the results of executed actions.
        '''

        # 2. Generate response from LLM
        print("Agent thinking...")
        response = generate_response(prompt)
        print(f"Agent response: {response} \n response end")
        

        # 3. Parse response to determine action
        action = parse_action(response)

        result = "Action executed"

        if action["tool_name"] == "list_files":
            result = {"result":list_files()}
        elif action["tool_name"] == "read_file":
            result = {"result":read_file(action["args"]["file_name"])}
        elif action["tool_name"] == "error":
            result = {"error":action["args"]["message"]}
        elif action["tool_name"] == "terminate":
            print(action["args"]["message"])
            break
        else:
            result = {"error":"Unknown action: "+action["tool_name"]}

        print(f"Action result: {result}")

        # 5. Update memory with response and results
        memory.extend([
            {"role": "assistant", "content": response},
            {"role": "user", "content": json.dumps(result)}
        ])

        # 6. Check termination condition
        if action["tool_name"] == "terminate":
            break

        iterations += 1