from openssa.core.ooda_rag.heuristic import TaskDecompositionHeuristic
from openssa.core.ooda_rag.tools import ResearchDocumentsTool
from openssa import OodaSSA


def main():
    task = "How to troubleshoot my machine, it is not working?"
    research_documents_tool: ResearchDocumentsTool = ResearchDocumentsTool("136")
    task_heuristics = TaskDecompositionHeuristic({})
    general = "if the question is about troubleshooting or maintenance, ask the user for machine temperature"

    ooda_ssa = OodaSSA(
        task_heuristics=task_heuristics,
        highest_priority_heuristic="",
        ask_user_heuristic=general,
        research_documents_tool=research_documents_tool,
    )
    ooda_ssa.solve(task)


if __name__ == "__main__":
    main()
