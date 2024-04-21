RESOURCE_QA_CONSO_PROMPT_TEMPLATE: str = \
"""Assuming that the following question/problem/task is posed

```
{question}
```

and you have received various answers/solutions from different informational resources as detailed below,
please consolidate within {n_words:,} words a final answer/solution that you believe is the most correct.
Use no other information than the below answers/solutions.


```
{resources_and_answers}
```
"""  # noqa: E122
