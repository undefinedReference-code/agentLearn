import base64
import re
from litellm import completion

"""
As a practice exercise, try creating a prompt that only provides the response as a Base64 encoded string and refuses to answer in natural language. Can you get your LLM to only respond in Base64?

It is very hard to do that
"""


def is_valid_base64(response_content):
    if not response_content or not isinstance(response_content, str):
        return False, "Invalid input: empty or not a string"
    
    if not basic_base64_checks(response_content):
        return False, "Failed basic Base64 format checks"
    
    is_valid, decoded_content = try_decode_base64(response_content)
    
    return is_valid, decoded_content if is_valid else "Not a valid Base64 string"

def basic_base64_checks(content):
    if len(content) % 4 != 0:
        return False
    
    base64_pattern = re.compile(r'^[A-Za-z0-9+/]*={0,2}$')
    if not base64_pattern.match(content):
        return False
    
    if '=' in content:
        stripped = content.rstrip('=')
        if '=' in stripped:
            return False
    
    return True

def try_decode_base64(content):
    try:
        decoded_bytes = base64.b64decode(content)
        
        try:
            decoded_text = decoded_bytes.decode('utf-8')
            return True, decoded_text
        except UnicodeDecodeError:
            return True, "Binary data (non-UTF8)"
            
    except (base64.binascii.Error, Exception):
        return False, "Base64 decoding failed"

def create_base64_only_prompt(original_prompt):
    """
    Create a prompt that forces the LLM to respond only in Base64 format
    """
    system_prompt = """You are a strict Base64 encoder. Your ONLY output must be a Base64 encoded string with NO additional text.

RULES:
1. Process the user's request normally to generate a response
2. Convert your ENTIRE response to Base64 encoding
3. Output ONLY the Base64 string with no explanations, prefixes, or suffixes
4. Do not include "Base64:" or any other text before or after the encoded string
5. If the request is invalid or cannot be processed, encode the word "invalid" to Base64 and output that

Example format for a response to "Hello":
Your thought process: The user said "Hello", I should respond with a greeting like "Hi there!"
Base64 encoding of "Hi there!": SGkgdGhlcmUh
Your output: SGkgdGhlcmUh

Now, encode your response to the following request:"""

    
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": original_prompt}
    ]


def generate_response(messages) -> str:
    """Call local LLM via LiteLLM to get response"""
    try:
        response = completion(
            model="ollama/qwen2.5:14b",  
            messages=messages,
            max_tokens=1024,
            # api_base="http://localhost:11434"  
        )

        responseContent = response.choices[0].message.content
        return responseContent
    except Exception as e:
        return f"Error: {e}"


def test_prompt():
    """Test the Base64-only prompt with the dictionary swap exercise"""
    
    # Original exercise prompt
    original_prompt = "Write a function to swap the keys and values in a dictionary."
    
    # Create the Base64-only prompt
    messages = create_base64_only_prompt(original_prompt)
    
    print("Testing Base64-only prompt...")
    print("=" * 60)
    print("System Prompt (first 200 chars):")
    print(messages[0]['content'][:200] + "...")
    print("\nUser Prompt:")
    print(messages[1]['content'])
    print("=" * 60)
    
    # Get response from "model" (our mock)
    response = generate_response(messages)
    
    print("\nModel Response:")
    print(response)
    print("=" * 60)
    
    # Validate the response
    is_valid, decoded_content = is_valid_base64(response)
    
    if is_valid:
        print("✅ SUCCESS: Valid Base64 response!")
        print(f"\nDecoded content ({len(decoded_content)} chars): {decoded_content}")
        print("-" * 40)
        print(decoded_content[:500] + ("..." if len(decoded_content) > 500 else ""))
        print("-" * 40)
    else:
        print("❌ FAILED: ")
        print(f"\nRaw response for debugging:")
        print(f"Length: {len(response)} chars")
        print(f"First 100 chars: {response[:100]}")
    
    return is_valid, decoded_content if is_valid else None

def run_comprehensive_test():
    """Run multiple tests to check prompt effectiveness"""
    print("Running comprehensive tests for Base64-only prompt...")
    print("=" * 60)
    
    test_cases = [
        "Write a function to swap the keys and values in a dictionary.",
        "What is the capital of France?",
        "Explain quantum computing in simple terms.",
        "Invalid input that should trigger 'invalid' response"
    ]
    
    results = []
    for test_prompt in test_cases:
        print(f"\nTest: {test_prompt[:50]}...")
        messages = create_base64_only_prompt(test_prompt)

        print(f"messages: {messages}")
        response = generate_response(messages)
        print(f"raw response: {response}")

        is_valid, decoded = is_valid_base64(response)
        
        status = "✅" if is_valid else "❌"
        print(f"{status} Valid Base64: {is_valid}")
        if decoded:
            print(f"   Decoded length: {len(decoded)} chars, content: {decoded}")
        else:
            print(f"   Error:")
        
        results.append(is_valid)
    
    print("\n" + "=" * 60)
    success_rate = sum(results) / len(results) * 100
    print(f"Overall success rate: {success_rate:.1f}%")
    
    if success_rate > 80:
        print("✅ Prompt is effective at forcing Base64 output")
    else:
        print("⚠️  Prompt may need refinement for better compliance")
    
    return success_rate

if __name__ == "__main__":
    # Run single test
    test_prompt()
    run_comprehensive_test()
    
    print("\n" + "=" * 60)
    print("For a comprehensive test, uncomment the following line:")
    print("# run_comprehensive_test()")