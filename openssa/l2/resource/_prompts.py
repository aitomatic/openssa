RESOURCE_OVERVIEW_PROMPT_TEMPLATE: str = (
    'Considering that your informational resource is named "{name}" (if that is helpful or relevant), '
    'identify the chief ENTITY/ENTITIES of interest, state the main TIME PERIOD(S) of interest, '
    'and give an overview of the key KINDS of INFO contained in your resource, '
    'without mentioning specific facts.'
)

RESOURCE_QA_PROMPT_TEMPLATE: str = (
"""Within {n_words:,} words, please answer the following question:

```
{question}
```

DO NOT include in your answer any examples/facts/numbers not concretely mentioned in your informational resource.
"""  # noqa: E122
)
