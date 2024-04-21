OBSERVE_PROMPT_TEMPLATE: str = \
"""Assuming that the following question/task is asked

```
{question}
```

and you have received various answers from different informational resources as detailed below,
please evaluate whether you can answer the posed question/task confidently with concrete results.

If you can answer confidently with concrete results, return a JSON dictionary
`{{"confident": true, "answer": "<fill in your answer using up to {n_words:,} words>"}}`.

If you cannot answer confidently with concrete results, return a JSON dictionary
`{{"confident": false}}`.

Please return ONLY the JSON DICTIONARY and no other text, not even the "```json" wrapping!

Use no other information than the below answers.


```
{resources_and_answers}
```
"""  # noqa: E122
