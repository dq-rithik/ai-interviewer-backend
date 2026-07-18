from abc import ABC, abstractmethod

class BaseAIProvider(ABC):
    """
    Abstract Base Class for AI Providers.
    All interchangeable providers (Groq, Gemini, OpenAI, Claude) must inherit from this
    and implement the question generation and interview evaluation methods.
    """
    
    @abstractmethod
    def generate_questions(self, profile: dict, config: dict) -> list:
        """
        Generate interview questions based on the candidate profile and interview configuration.
        
        :param profile: dict containing 'fullName', 'jobRole', 'experienceLevel', 'skills'
        :param config: dict containing 'interviewType', 'difficulty', 'numQuestions'
        :return: list of dicts, each matching the schema:
                 {
                   "id": int,
                   "question": str,
                   "type": "descriptive" | "mcq" | "coding" | "scenario",
                   "difficulty": str,
                   "expected_topics": list[str],
                   "options": list[str] (only for MCQ),
                   "correct_option": str (only for MCQ, e.g. "A", "B", "C", "D" or exact text)
                 }
        """
        pass
        
    @abstractmethod
    def evaluate_interview(self, profile: dict, config: dict, questions: list, answers: dict) -> dict:
        """
        Evaluate a completed interview and generate a final report.
        
        :param profile: dict containing candidate details
        :param config: dict containing interview configuration
        :param questions: list of generated questions
        :param answers: dict mapping question id (str) to candidate's answer
        :return: dict conforming to the detailed evaluation report schema
        """
        pass
