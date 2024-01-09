from openssa.core.ooda_rag.heuristic import TaskDecompositionHeuristic
from openssa.core.ooda_rag.tools import ResearchDocumentsTool
from openssa import OodaSSA

# TODO: fix case empty ooda task result for simple question


def main():
    # task = "what can you do?"
    task = "How to start the machine EOS M290?"
    research_documents_tool: ResearchDocumentsTool = ResearchDocumentsTool("251")
    task_heuristics = TaskDecompositionHeuristic({})

    ooda_ssa = OodaSSA(
        task_heuristics=task_heuristics,
        highest_priority_heuristic="priority",
        ask_user_heuristic="",
        research_documents_tool=research_documents_tool,
        enable_generative=True,
    )
    answer = ooda_ssa.solve(task)
    print(answer)


if __name__ == "__main__":
    main()
