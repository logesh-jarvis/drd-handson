import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from typing import Dict, Any

load_dotenv()

anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_coding_question() -> Dict[str, Any]:
    prompt = f"""{HUMAN_PROMPT}
Generate a coding question about random programming topics like data structures and algorithms. The response should be in JSON format with the following structure:
{{
    "question": "The full text of the question",
    "difficulty": "easy|medium|hard",
    "category": "data structures|algorithms|general programming",
    "hints": ["Hint 1", "Hint 2"],
    "solution": "A brief solution or approach to solve the problem",
    "test_cases": [
        {{"input": "Sample input 1", "expected_output": "Expected output 1"}},
        {{"input": "Sample input 2", "expected_output": "Expected output 2"}},
        {{"input": "Sample input 3", "expected_output": "Expected output 3"}}
    ]
}}
Ensure all fields are filled appropriately, including at least 3 sample test cases.
Enclose the entire JSON response within backticks (`).
Do not include any additional text or explanations outside the backticks.
{AI_PROMPT}"""
    
    try:
        completion = anthropic.completions.create(
            model="claude-2",
            max_tokens_to_sample=1500,
            prompt=prompt
        )
        
        # Extract content within backticks
        json_content = extract_json_from_backticks(completion.completion)
        if not json_content:
            raise ValueError("Failed to extract JSON content from the response")

        response = json.loads(json_content)
        
        # Validate the response structure
        validate_response_structure(response)
        
        return response
    except json.JSONDecodeError:
        return create_error_response("Invalid JSON response")
    except ValueError as ve:
        return create_error_response(str(ve))
    except Exception as e:
        return create_error_response(f"An unexpected error occurred: {str(e)}")

def extract_json_from_backticks(text: str) -> str:
    parts = text.split('`')
    if len(parts) >= 3:
        return parts[1]
    return ""

def validate_response_structure(response: Dict[str, Any]):
    required_fields = ["question", "difficulty", "category", "hints", "solution", "test_cases"]
    for field in required_fields:
        if field not in response:
            raise ValueError(f"Missing required field: {field}")
    
    if not isinstance(response["hints"], list):
        raise ValueError("Hints should be a list")
    
    if not isinstance(response["test_cases"], list) or len(response["test_cases"]) < 3:
        raise ValueError("Test cases should be a list with at least 3 items")
    
    for test_case in response["test_cases"]:
        if "input" not in test_case or "expected_output" not in test_case:
            raise ValueError("Each test case should have 'input' and 'expected_output'")

def create_error_response(message: str) -> Dict[str, str]:
    return {
        "status": "error",
        "message": message
    }

if __name__ == "__main__":
    result = generate_coding_question()
    print(json.dumps(result, indent=2))