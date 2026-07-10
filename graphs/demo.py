from graphs.research_graph import ResearchGraph
from graphs.state import WorkflowState
from pprint import pprint

graph = ResearchGraph().build()

state = WorkflowState(
    topic="AI Applications in Agriculture"
)

result = graph.invoke(state)

print(result["report"])
