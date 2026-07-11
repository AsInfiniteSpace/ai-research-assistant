from openai import OpenAI

from config import settings
from services.logger import logger
from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class AIService:
    """
    Centralized service for interacting with OpenAI models.
    """

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.MODEL_NAME

        logger.info(f"AIService initialized with model: {self.model}")

    def generate(
    self,
    system_prompt: str,
    user_prompt: str,
    response_model: Type[BaseModel] | None = None,
    ):
        """
        Generate either plain text or a structured response.
        """

        logger.info("Sending request to OpenAI...")

        try:
            if response_model is None:
                response = self.client.responses.create(
                    model=self.model,
                    instructions=system_prompt,
                    input=user_prompt,
                )

                logger.info("Text response received successfully.")

                return response.output_text

            response = self.client.responses.parse(
                model=self.model,
                instructions=system_prompt,
                input=user_prompt,
                text_format=response_model,
            )

            """logger.info(response.usage)

            logger.info(response.model_dump())"""
            

            logger.info("Structured response received successfully.")

            return response.output_parsed

        except Exception:
            logger.exception("Error while calling OpenAI.")
            raise