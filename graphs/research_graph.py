from graphs.state import WorkflowState

from agents.planner.agent import PlannerAgent
from agents.search.agent import SearchAgent
from agents.writer.agent import WriterAgent

from langgraph.graph import StateGraph, START, END

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

        for task in state.plan.tasks:
            results.append(
                self.search.search(task)
            )

        state.search_results = results

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

        return state

    def build(self):
        
        """
        Build and compile the research graph.
        """
        builder = StateGraph(WorkflowState)
        
        builder.add_node(
        "planner",
        self.planner_node,
        )

        builder.add_node(
            "search",
            self.search_node,
        )

        builder.add_node(
            "writer",
            self.writer_node,
        )

        builder.add_edge(
        START,
        "planner",
        )

        builder.add_edge(
            "planner",
            "search",
        )

        builder.add_edge(
            "search",
            "writer",
        )

        builder.add_edge(
            "writer",
            END,
        )

        return builder.compile()