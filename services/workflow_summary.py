from services.logger import logger
from graphs.state import WorkflowState

def log_workflow_summary(state, elapsed_time: float):
    """
    Log a concise workflow summary.
    """
    if isinstance(state, dict):
        state = WorkflowState.model_validate(state)

    logger.info("=" * 55)
    logger.info("AI Workflow Summary")
    logger.info("=" * 55)

    logger.info(f"Topic               : {state.topic}")
    logger.info(
        f"Memory              : {'HIT' if state.memory_hit else 'MISS'}"
    )
    logger.info(f"Retries            : {state.retry_count}")

    if state.evaluation:
        logger.info(
            f"Evaluation Score    : {state.evaluation.score}/10"
        )

    if state.plan:
        logger.info(
            f"Search Tasks        : {len(state.plan.tasks)}"
        )

    logger.info(
        f"Search Result Groups: {len(state.search_results)}"
    )

    logger.info(
        f"Workflow Time       : {elapsed_time:.2f} sec"
    )

    logger.info("=" * 55)