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

class OpenAIProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        self.endpoint = "https://api.openai.com/v1/chat/completions"
        
    def _call_api(self, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            raise ValueError("OpenAI API Key is not configured.")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.3,
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(self.endpoint, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            res_json = response.json()
            return res_json["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as e:
            raise Exception(f"OpenAI API call failed: {str(e)} - {response.text}")
        except Exception as e:
            raise Exception(f"OpenAI API call failed: {str(e)}")

    def generate_questions(self, profile: dict, config: dict) -> list:
        user_prompt = get_question_gen_user_prompt(profile, config)
        response_text = self._call_api(QUESTION_GEN_SYSTEM_PROMPT, user_prompt)
        parsed = parse_json_response(response_text)
        return parsed.get("questions", [])

    def evaluate_interview(self, profile: dict, config: dict, questions: list, answers: dict) -> dict:
        user_prompt = get_evaluation_user_prompt(profile, config, questions, answers)
        response_text = self._call_api(EVALUATION_SYSTEM_PROMPT, user_prompt)
        return parse_json_response(response_text)
