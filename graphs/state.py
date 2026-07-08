from pydantic import BaseModel, Field

from agents.planner.models import ResearchPlan
from agents.search.models import SearchResults
from agents.writer.models import ResearchReport

class WorkflowState(BaseModel):
    """
    Shared state passed between LangGraph nodes.
    """

    topic: str

    plan: ResearchPlan | None = None

    search_results: list[SearchResults] = Field(default_factory=list)

    report: ResearchReport | None = None