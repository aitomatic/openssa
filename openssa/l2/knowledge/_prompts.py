from openssa.l2.util.lm.abstract import LMChatHist


KNOWLEDGE_INJECTION_PROMPT_TEMPLATE: str = \
"""PLEASE ADD THE FOLLOWING TO YOUR KNOWLEDGE TO BE USED IN PLANNING, REASONING & PROBLEM SOLVING:

START OF KNOWLEDGE PIECE >>>
****************************


{knowledge}


****************************
<<< END OF KNOWLEDGE PIECE
"""  # noqa: E122


def knowledge_injection_lm_chat_msgs(knowledge: set[str]) -> LMChatHist:
    return [{'role': 'system', 'content': KNOWLEDGE_INJECTION_PROMPT_TEMPLATE.format(knowledge=k)}
            for k in knowledge]
