from graphs.research_graph import ResearchGraph
from graphs.state import WorkflowState
from pprint import pprint

graph = ResearchGraph().build()

state = WorkflowState(
    topic="Environmental effects of AI"
)

result = graph.invoke(state)

print(result["report"])
