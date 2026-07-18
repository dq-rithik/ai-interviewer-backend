import requests
from app.services.ai.base_provider import BaseAIProvider
from app.services.ai.prompts import (
    QUESTION_GEN_SYSTEM_PROMPT, 
    get_question_gen_user_prompt,
    EVALUATION_SYSTEM_PROMPT,
    get_evaluation_user_prompt
)
from app.utils.json_parser import parse_json_response
from app.config import Config

class ClaudeProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = Config.CLAUDE_API_KEY
        self.model = Config.CLAUDE_MODEL
        self.endpoint = "https://api.anthropic.com/v1/messages"
        
    def _call_api(self, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            raise ValueError("Claude API Key is not configured.")
            
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 4000,
            "temperature": 0.3
        }
        
        try:
            response = requests.post(self.endpoint, headers=headers, json=payload, timeout=40)
            response.raise_for_status()
            res_json = response.json()
            return res_json["content"][0]["text"]
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Claude API call failed: {str(e)} - {response.text}")
        except Exception as e:
            raise Exception(f"Claude API call failed: {str(e)}")

    def generate_questions(self, profile: dict, config: dict) -> list:
        user_prompt = get_question_gen_user_prompt(profile, config)
        response_text = self._call_api(QUESTION_GEN_SYSTEM_PROMPT, user_prompt)
        parsed = parse_json_response(response_text)
        return parsed.get("questions", [])

    def evaluate_interview(self, profile: dict, config: dict, questions: list, answers: dict) -> dict:
        user_prompt = get_evaluation_user_prompt(profile, config, questions, answers)
        response_text = self._call_api(EVALUATION_SYSTEM_PROMPT, user_prompt)
        return parse_json_response(response_text)
