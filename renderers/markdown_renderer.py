from agents.writer.models import ResearchReport


class MarkdownRenderer:
    """
    Renders a ResearchReport into formatted Markdown.
    """

    @staticmethod
    def render(report: ResearchReport) -> str:
        return (
            f"# {report.title}\n\n"
            f"## Executive Summary\n\n"
            f"{report.executive_summary}\n\n"
            f"{report.report}"
        )