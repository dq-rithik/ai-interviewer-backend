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

class GeminiProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.model = Config.GEMINI_MODEL
        
    def _call_api(self, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            raise ValueError("Gemini API Key is not configured.")
            
        # Standard v1beta endpoint for generateContent
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "systemInstruction": {
                "parts": [
                    {"text": system_prompt}
                ]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": user_prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.3,
                "responseMimeType": "application/json"
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            res_json = response.json()
            # Extract content from response structure
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Gemini API call failed: {str(e)} - {response.text}")
        except Exception as e:
            raise Exception(f"Gemini API call failed: {str(e)}")

    def generate_questions(self, profile: dict, config: dict) -> list:
        user_prompt = get_question_gen_user_prompt(profile, config)
        response_text = self._call_api(QUESTION_GEN_SYSTEM_PROMPT, user_prompt)
        parsed = parse_json_response(response_text)
        return parsed.get("questions", [])

    def evaluate_interview(self, profile: dict, config: dict, questions: list, answers: dict) -> dict:
        user_prompt = get_evaluation_user_prompt(profile, config, questions, answers)
        response_text = self._call_api(EVALUATION_SYSTEM_PROMPT, user_prompt)
        return parse_json_response(response_text)
