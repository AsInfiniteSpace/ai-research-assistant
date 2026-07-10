from pydantic import BaseModel, Field

from agents.planner.models import ResearchPlan
from agents.search.models import SearchResults
from agents.writer.models import ResearchReport
from agents.evaluator.models import SearchEvaluation

class WorkflowState(BaseModel):
    """
    Shared state passed between LangGraph nodes.
    """

    topic: str

    plan: ResearchPlan | None = None

    search_results: list[SearchResults] = Field(default_factory=list)

    report: ResearchReport | None = None

    memory_hit: bool = False

    """cached_report: ResearchReport | None = None"""

    retry_count: int = 0

    max_retries: int = 2

    evaluation: SearchEvaluation | None = None