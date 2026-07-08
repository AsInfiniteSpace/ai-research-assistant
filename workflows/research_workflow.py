from agents.planner.agent import PlannerAgent
from agents.planner.models import ResearchPlan
from agents.search.agent import SearchAgent
from agents.search.models import SearchResults
from services.logger import logger
from agents.writer import WriterAgent
from agents.writer.models import ResearchReport
from services.memory_service import MemoryService


class ResearchWorkflow:
    """
    Coordinates the research process.
    """

    def __init__(self):
        self.planner = PlannerAgent()
        self.search = SearchAgent()
        self.writer = WriterAgent()
        self.memory = MemoryService()

    def run(
        self,
        topic: str,
    ) -> ResearchReport:
        """
        Execute the research workflow.
        """
        memories = self.memory.retrieve(topic, top_k=1)

        if memories:
            logger.info("Memory hit. Skipping web research.")

            return ResearchReport(
                title=f"Cached Research: {topic}",
                executive_summary="Retrieved from long-term memory.",
                report=memories[0],
            )

        logger.info("Memory miss. Starting new research.")

        plan = self.planner.create_plan(topic)

        search_results = []

        for task in plan.tasks:
            try:
                results = self.search.search(task)
                search_results.append(results)

            except Exception:
                logger.exception(
                    f"Search failed for task: {task.title}"
                )
        logger.info(
            f"Completed searches for {len(search_results)} "
            f"out of {len(plan.tasks)} tasks."
        )
        report = self.writer.write(
            topic=topic,
            search_results=search_results,
        )
        self.memory.save(
        topic=topic,
        content=report.report,
        )
        return report