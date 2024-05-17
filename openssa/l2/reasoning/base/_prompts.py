from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openssa.l2.reasoning.abstract import AskAnsPair


RESOURCE_QA_CONSO_PROMPT_TEMPLATE: str = \
"""Assuming that the following question/problem/task is posed

```
{question}
```

and you have received various answers/solutions from different informational resources as detailed below,
please consolidate within {n_words:,} words a final answer/solution that you believe is the most correct.


```
{resources_and_answers}
```
"""  # noqa: E122


RESOURCE_QA_AND_OTHER_RESULTS_CONSO_PROMPT_TEMPLATE: str = \
"""Assuming that the following question/problem/task is posed

```
{question}
```

and you have received various answers/solutions from different informational resources
as well as auxiliary information from other sources as detailed below,
please consolidate within {n_words:,} words a final answer/solution that you believe is the most correct.


```
{resources_and_answers}


{other_results}
```
"""  # noqa: E122


OTHER_RESULTS_CONSO_PROMPT_TEMPLATE: str = \
"""Assuming that the following question/problem/task is posed

```
{question}
```

and you have received auxiliary information from other sources as detailed below,
please consolidate within {n_words:,} words a final answer/solution that you believe is the most correct.


```
{other_results}
```
"""  # noqa: E122


def format_other_result(other_result: AskAnsPair) -> str:
    question, answer = other_result
    return (f'======================\n'
            'ADDITIONAL INFORMATION:\n'
            '\n'
            'QUESTION:\n'
            '-----------------------\n'
            f'{question}\n'
            '-----------------------\n'
            '\n'
            'ANSWER:\n'
            '-----------------------\n'
            f'{answer}\n'
            '-----------------------\n'
            '=======================\n')
