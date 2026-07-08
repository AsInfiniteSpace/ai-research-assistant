from agents.base import BaseAgent
from agents.planner.models import ResearchTask
from agents.search.models import SearchResult, SearchResults, SearchQuery
from tools.search_tool import SearchTool
from services.logger import logger



class SearchAgent(BaseAgent):
    """
    Responsible for searching information
    for a research task.
    """

    def __init__(self):
        super().__init__("search_query.txt")

        self.search_tool = SearchTool()

    def search(self, task: ResearchTask) -> SearchResults:
        """
        Execute a web search for a research task.
        """

        search_query = self.generate_search_query(task)
        
        raw_results = self.search_tool.execute(
            search_query.query
        )

        results = [
            SearchResult(**item)
            for item in raw_results
        ]

        return SearchResults(
            query=search_query.query,
            results=results,
        )

    def generate_search_query(
            self,
            task: ResearchTask,
        ) -> SearchQuery:

        """
        Generate an optimized web search query.
        """

        logger.info(
            f"Generating search query for task: {task.title}"
        )

        user_prompt = (
            f"Research Task:\n\n"
            f"{task.title}\n\n"
            f"{task.description}"
        )

        search_query = self.ai_service.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            response_model=SearchQuery,
        )

        logger.info(
            f"Generated search query: {search_query.query}"
        )

        return search_query