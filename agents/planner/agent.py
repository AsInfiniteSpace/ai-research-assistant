from agents.base import BaseAgent
from agents.planner.models import ResearchPlan


class PlannerAgent(BaseAgent):
    """
    Responsible for creating structured research plans.
    """

    def __init__(self):
        super().__init__("planner.txt")

    def create_plan(self, topic: str) -> ResearchPlan:
        return self.ai_service.generate(
            system_prompt=self.system_prompt,
            user_prompt=topic,
            response_model=ResearchPlan,
        )