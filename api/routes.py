from fastapi import APIRouter, HTTPException
from api.models import HealthResponse


from graphs.research_graph import ResearchGraph
from graphs.state import WorkflowState

from api.models import ResearchRequest
from agents.writer.models import ResearchReport

from services.logger import logger

router = APIRouter()

graph = ResearchGraph().compile()

@router.get(
    "/health",
    response_model=HealthResponse,
)


def health():
    """
    Health check endpoint.
    """

    return HealthResponse(
        status="healthy",
    )

@router.post(
    "/research",
    response_model=ResearchReport,
)
def research(request: ResearchRequest):
    """
    Generate a research report.
    """

    try:
        state = WorkflowState(
            topic=request.topic,
        )

        result = graph.invoke(state)

        if isinstance(result, dict):
            result = WorkflowState.model_validate(result)

        return result.report

    except Exception as e:
        logger.exception("Research workflow failed.")

        raise HTTPException(
            status_code=500,
            detail="Failed to generate research report.",
        )

@router.get("/")
def root():
    return {
        "message": "Multi-Agent AI Research Assistant API",
        "version": "1.0.0",
    }