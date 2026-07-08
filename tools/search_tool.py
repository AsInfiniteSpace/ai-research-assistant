from tavily import TavilyClient

from config import settings
from tools.base_tool import BaseTool
from services.logger import logger


class SearchTool(BaseTool):
    """
    Tool responsible for searching the web.
    """

    def __init__(self):
        super().__init__("Web Search")

        self.client = TavilyClient(
            api_key=settings.TAVILY_API_KEY
        )

    def execute(self, query: str):
        """
        Execute a web search.
        """

        self.log_execution()

        try:
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=2,
            )

            normalized_results = []

            for item in response.get("results", []):
                normalized_results.append(
                    {
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "snippet": item.get("content", ""),
                    }
                )

            logger.info(
                f"Retrieved {len(normalized_results)} search results."
            )

            return normalized_results

        except Exception as e:
            logger.exception("Search failed.")
            raise