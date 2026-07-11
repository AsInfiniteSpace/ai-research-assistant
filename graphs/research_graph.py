from graphs.state import WorkflowState

from agents.planner.agent import PlannerAgent
from agents.search.agent import SearchAgent
from agents.writer.agent import WriterAgent
from agents.evaluator.agent import EvaluatorAgent
from services.timer import Timer

from langgraph.graph import StateGraph, START, END
from services.memory_service import MemoryService

from services.logger import logger

class ResearchGraph:
    """
    LangGraph implementation of the
    research workflow.
    """
    def __init__(self):
        self.planner = PlannerAgent()
        self.search = SearchAgent()
        self.writer = WriterAgent()
        self.memory = MemoryService()
        self.evaluator = EvaluatorAgent()
        self.timer = Timer()
        
    
    def memory_node(
    self,
    state: WorkflowState,
    ) -> WorkflowState:
        """
        Check whether a report already exists.
        """

        logger.info("Running Memory Node")

        report = self.memory.retrieve(
            state.topic
        )

        if report is not None:
            logger.info("Memory hit.")

            state.memory_hit = True
            state.report = report

        else:
            logger.info("Memory miss.")

        logger.info(
            f"Memory Node completed in {self.timer.elapsed():.2f} seconds"
        )
        return state

    def planner_node(
    self,
    state: WorkflowState,
    ) -> WorkflowState:
        """
        Generate a research plan.
        """

        logger.info("Running Planner Node")

        state.plan = self.planner.create_plan(
            state.topic
        )
        logger.info(
            f"Planner Node completed in {self.timer.elapsed():.2f} seconds"
        )
        return state

    def search_node(
    self,
    state: WorkflowState,
    ) -> WorkflowState:
        """
        Execute searches.
        """

        logger.info("Running Search Node")

        results = []

        feedback = None

        if (
            state.evaluation is not None
            and not state.evaluation.success
        ):
            feedback = state.evaluation.reasoning

        for task in state.plan.tasks:
            results.append(
                self.search.search(
                    task,
                    feedback,
                )
            )

        state.search_results = results
        logger.info(
            f"Search Node completed in {self.timer.elapsed():.2f} seconds"
        )
        return state    

    def writer_node(
    self,
    state: WorkflowState,
    ) -> WorkflowState:
        """
        Generate the report.
        """

        logger.info("Running Writer Node")

        state.report = self.writer.write(
            topic=state.topic,
            search_results=state.search_results,
        )
        
        logger.info(
            f"Writer Node completed in {self.timer.elapsed():.2f} seconds"
        )
        return state

    def save_memory_node(
    self,
    state: WorkflowState,
    ) -> WorkflowState:

        logger.info("Running Save Memory Node")

        self.memory.save(
            topic=state.topic,
            report=state.report,
        )
        logger.info(
            f"Save Memory Node completed in {self.timer.elapsed():.2f} seconds"
        )
        return state

    def evaluate_search_node(
    self,
    state: WorkflowState,
    ) -> WorkflowState:
        """
        Evaluate whether search results are good enough.
        """

        logger.info("Running Search Evaluator Node")
        evaluation = self.evaluator.evaluate(
            topic=state.topic,
            search_results=state.search_results,
        )

        state.evaluation = evaluation

        logger.info(
            f"Evaluation Score: {evaluation.score}/10"
        )
        logger.info(
            f"Evaluation Success: {evaluation.success}"
        )

        logger.info(
            f"Evaluation Serach Node completed in {self.timer.elapsed():.2f} seconds"
        )
        return state

    def increment_retry_node(
    self,
    state: WorkflowState,
    ) -> WorkflowState:

        logger.info(
            f"Retrying search ({state.retry_count + 1}/{state.max_retries})"
        )
        
        logger.info("Evaluator Feedback:")
        logger.info(state.evaluation.reasoning)
        

        state.retry_count += 1

        return state


    def compile(self):
        
        """
        Build and compile the research graph.
        """
        builder = StateGraph(WorkflowState)
        
        builder.add_node(
            "memory",
            self.memory_node,
        )

        builder.add_node(
            "planner",
            self.planner_node,
        )

        builder.add_node(
            "search",
            self.search_node,
        )

        builder.add_node(
            "evaluate_search",
            self.evaluate_search_node,
        )

        builder.add_node(
            "writer",
            self.writer_node,
        )
        builder.add_node(
            "save_memory",
            self.save_memory_node,
        )
        builder.add_node(
            "increment_retry",
            self.increment_retry_node,
        )
        """builder.add_edge(
        START,
        "planner",
        )"""
        builder.add_edge(
            START,
            "memory",
        )
        builder.add_conditional_edges(
            "memory",
            self.should_plan,
        )

        builder.add_edge(
            "planner",
            "search",
        )

        builder.add_edge(
            "search",
            "evaluate_search",
        )

        builder.add_conditional_edges(
            "evaluate_search",
            self.should_retry_search,
        )

        builder.add_edge(
            "increment_retry",
            "search",
        )

        builder.add_edge(
            "writer",
            "save_memory",
        )

        builder.add_edge(
            "save_memory",
            END,
        )

        return builder.compile()

    """First router funciton"""
    def should_plan(
    self,
    state: WorkflowState,
    ) -> str:
        """
        Decide whether planning is needed.
        """

        logger.info("Routing...")

        if state.memory_hit:
            return END
        
        return "planner"

    
    def should_retry_search(
    self,
    state: WorkflowState,
    ):
        if state.evaluation is None:
            return "increment_retry"

        if state.evaluation.success:
            return "writer"

        if state.retry_count < state.max_retries:
            return "increment_retry"

        return "writer"