from pydantic import BaseModel


class SearchEvaluation(BaseModel):
    """
    Evaluation of search quality.
    """

    success: bool

    score: int

    reasoning: str