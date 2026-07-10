from agents.base import BaseAgent

from agents.evaluator.models import SearchEvaluation

import json

from services.logger import logger

class EvaluatorAgent(BaseAgent):
    """
    Evaluates search quality.
    """

    def __init__(self):
        super().__init__("evaluator.txt")

    def evaluate(
        self,
        topic: str,
        search_results,
    ) -> SearchEvaluation:
        evidence = []

        for result in search_results:
            evidence.append(
                {
                    "query": result.query,
                    "results": [
                        {
                            "title": item.title,
                            "snippet": item.snippet,
                            "url": item.url,
                        }
                        for item in result.results
                    ],
                }
            )
        
        user_prompt = (
            f"Research Topic:\n{topic}\n\n"
            f"Search Results:\n"
            f"{json.dumps(evidence, indent=2)}"
        )

        evaluation = self.ai_service.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            response_model=SearchEvaluation,
        )

        return evaluation