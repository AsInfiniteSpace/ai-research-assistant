from pydantic import BaseModel


class ResearchRequest(BaseModel):
    """
    Incoming API request.
    """

    topic: str


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str