from pathlib import Path


class PromptManager:
    """
    Loads prompt templates from the prompts directory.
    """

    BASE_PATH = Path("prompts")

    @classmethod
    def load(cls, category: str, filename: str) -> str:
        """
        Load a prompt file.

        Example:
            PromptManager.load("system", "planner.txt")
        """

        path = cls.BASE_PATH / category / filename

        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")

        return path.read_text(encoding="utf-8")