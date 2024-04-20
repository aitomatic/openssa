RESOURCE_QA_CONSO_PROMPT_TEMPLATE: str = \
"""Assuming that the following question/task is asked

```
{question}
```

and you have received various answers from different informational resources as detailed below,
please consolidate within {n_words:,} words a final answer that you believe is the most correct.
Use no other information than the below answers.


```
{resources_and_answers}
```
"""  # noqa: E122
