import json
import re

def parse_json_response(raw_text: str):
    """
    Cleans up the raw text from an AI provider response, stripping out markdown
    code block wrappers (like ```json ... ```) and extracting the JSON content.
    """
    cleaned = raw_text.strip()
    
    # Remove markdown code blocks (```json ... ``` or ``` ... ```)
    match = re.search(r'```(?:json)?\s*(.*?)\s*```', cleaned, re.DOTALL | re.IGNORECASE)
    if match:
        cleaned = match.group(1).strip()
        
    # Find the outermost curly braces to extract raw JSON if the model appended pre/post text
    start_idx = cleaned.find('{')
    end_idx = cleaned.rfind('}')
    
    if start_idx != -1 and end_idx != -1:
        cleaned = cleaned[start_idx:end_idx + 1]
        
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON returned from AI model. Error: {str(e)}. Content:\n{raw_text}")
