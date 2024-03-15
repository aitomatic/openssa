import pandas as pd
from openssa.core.ooda_rag.rag_ooda import RagOODA
from openssa.core.ooda_rag.tools import ResearchDocumentsTool


DATA_FOLDER_PATH = "examples/data"


def load_agent():
    return ResearchDocumentsTool("251")  # M290


def main():
    agent_tool = load_agent()

    resources = [agent_tool]

    questions = [
        "do I need heat treatment for the 316L with M290?",
        "Which steel can I print?",
        # "can I print a part 50 cm long in the M290?",
        # "Is it preferable to use nitrogen when printing with titanium?",
        # "List all the materials I can print with?",
        # "What are the calibration steps for a new build?",
        # "what are the size limits?",
        # "what are the parts size limits for the M290?",
    ]

    agent_answers = []
    ro_answers = []

    for q in questions:
        print(f"\nQuestion: {q}\n")
        agent_answer = agent_tool.execute(q).get("content", "")
        agent_answers.append(agent_answer)
        rag_ooda = RagOODA(resources=resources)
        rag_ooda_answer = rag_ooda.chat_with_agent(q)
        ro_answers.append(rag_ooda_answer)

    df = pd.DataFrame(  # noqa: PD901
        {
            "question": questions,
            "standard agent": agent_answers,
            "rag ooda": ro_answers,
        }
    )
    df.to_csv(f"{DATA_FOLDER_PATH}/qa_standard_agent_comparion.csv", index=False)


if __name__ == "__main__":
    main()
