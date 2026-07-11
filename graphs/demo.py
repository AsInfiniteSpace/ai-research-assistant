from graphs.research_graph import ResearchGraph
from graphs.state import WorkflowState
from pprint import pprint
from services.timer import Timer
from renderers.markdown_renderer import MarkdownRenderer
from services.logger import logger
from agents.writer.models import ResearchReport
from services.workflow_summary import log_workflow_summary
from utils.report_exporter import ReportExporter


graph = ResearchGraph().compile()
exporter = ReportExporter()

timer = Timer()

state = WorkflowState(
    topic="AI in Quantum Computing"
)

result = graph.invoke(state)

logger.info(
    f"Workflow completed in {timer.elapsed():.2f} seconds"
)

log_workflow_summary(
    result,
    timer.elapsed(),
)
"""print(
    MarkdownRenderer.render(
        result["report"]
    )
)"""
report = ResearchReport.model_validate(
    result["report"]
)
path = exporter.export(report)

print("\n" + "=" * 60)
print("Report successfully exported.")
print(f"Location: {path}")
print("=" * 60)

print(
    MarkdownRenderer.render(report)
)