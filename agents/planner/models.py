from pydantic import BaseModel, Field


class ResearchTask(BaseModel):
    """
    Represents one research task.
    """

    title: str = Field(
        description="Short title of the task."
    )

    description: str = Field(
        description="Detailed explanation of what should be researched."
    )

    priority: int = Field(
    ge=1,
    le=10,
    description="Execution priority from 1 (highest) to 10 (lowest)."
    )


class ResearchPlan(BaseModel):
    """
    Complete research plan.
    """

    topic: str

    tasks: list[ResearchTask]