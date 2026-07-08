from workflows.research_workflow import ResearchWorkflow


def main():
    workflow = ResearchWorkflow()

    report = workflow.run(
        "Future of AI in Healthcare"
    )

    print("\n")
    print("=" * 80)
    print(report.title)
    print("=" * 80)
    print(report.report)

    """print("\n===== PLAN =====\n")
    print(plan)

    print("\n===== SEARCH RESULTS =====\n")

    for result in search_results:
        print(result)
        print()
    """

if __name__ == "__main__":
    main()