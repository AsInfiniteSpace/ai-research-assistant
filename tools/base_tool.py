from services.logger import logger
from abc import ABC, abstractmethod

class BaseTool(ABC):
    """
    Base class for all tools.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Execute the tool.
        """
        pass

    def log_execution(self):
        logger.info(f"Executing tool: {self.name}")