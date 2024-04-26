from openssa.core.ooda_rag.heuristic import TaskDecompositionHeuristic
from openssa.core.ooda_rag.tools import ResearchDocumentsTool
from openssa import OodaSSA
from openssa.core.ooda_rag.builtin_agents import AskUserAgentV2


def conversation_test():
    ask_user_heuristic = "ask about the machine status and temperature and pressure when user asks about troubleshooting or maintenance"
    conversation = [
        {
            "role": "user",
            "content": "How to troubleshoot my machine, it is not working?",
        },
    ]
    while True:
        ask_user_agent = AskUserAgentV2(
            ask_user_heuristic=ask_user_heuristic, conversation=conversation
        )
        result = ask_user_agent.execute()
        print(result)
        conversation.append({"role": "assistant", "content": result})
        rep = input("user: ")
        conversation.append({"role": "user", "content": rep})


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
