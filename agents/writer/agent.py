from agents.base import BaseAgent
from agents.writer.models import ResearchReport
from agents.search.models import SearchResults
import json

from services.logger import logger


class WriterAgent(BaseAgent):
    """
    Generates the final research report.
    """

    def __init__(self):
        super().__init__("writer.txt")

    


    def write(self, topic: str, search_results: list[SearchResults],) -> ResearchReport:
        """
        Generate the final research report.
        """

        logger.info("Generating research report...")

        evidence = []

        source_id = 1

        for result in search_results:
            result_sources = []

            for item in result.results:
                result_sources.append(
                    {
                        "source_id": source_id,
                        "title": item.title,
                        "url": item.url,
                        "snippet": item.snippet,
                    }
                )

                source_id += 1

            evidence.append(
                {
                    "query": result.query,
                    "sources": result_sources,
                }
            )
                    
            logger.info(
                f"Preparing report from {len(search_results)} search result groups."
            )

            user_prompt = (
                f"Research Topic:\n{topic}\n\n"
                f"Research Findings:\n"
                f"{json.dumps(evidence, indent=2)}"
            )

            report = self.ai_service.generate(
                system_prompt=self.system_prompt,
                user_prompt=user_prompt,
                response_model=ResearchReport,
            )

            logger.info("Research report generated successfully.")

            return report