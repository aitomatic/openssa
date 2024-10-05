from openssa.core.util.lm.base import LMChatHist

from .base import Knowledge


KNOWLEDGE_INJECTION_PROMPT_TEMPLATE: str = \
"""PLEASE ADD THE FOLLOWING TO YOUR KNOWLEDGE TO BE USED IN PLANNING, REASONING & PROBLEM SOLVING:

START OF KNOWLEDGE PIECE >>>
****************************


{knowledge}


****************************
<<< END OF KNOWLEDGE PIECE
"""  # noqa: E122


def knowledge_injection_lm_chat_msgs(knowledge: set[Knowledge]) -> LMChatHist:
    assert isinstance(knowledge, set | list | tuple), TypeError('*** KNOWLEDGE MUST BE COLLECTION OF STRINGS ***')

    return [{'role': 'system', 'content': KNOWLEDGE_INJECTION_PROMPT_TEMPLATE.format(knowledge=k)}
            for k in knowledge]
