from services.ai_service import AIService
from services.prompt_manager import PromptManager


class BaseAgent:
    """
    Base class for all AI agents.
    """

    def __init__(self, system_prompt_file: str):
        self.ai_service = AIService()

        self.system_prompt = PromptManager.load(
            "system",
            system_prompt_file,
        )