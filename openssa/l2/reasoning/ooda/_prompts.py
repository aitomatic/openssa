OBSERVE_PROMPT_TEMPLATE: str = \
"""Assuming that the following question/task is asked

```
{question}
```

and you have received various answers from different informational resources as detailed below,
please evaluate whether you can answer the posed question/task confidently with concrete results.
If the question/task mentions any RIGOROUS BASES/CRITERIA/DEFINITIONS for judgement,
the concrete results MUST RESPOND TO SUCH BASES/CRITERIA/DEFINITIONS for the answer to be considered confident.
If the question/task involves any NUMERICAL QUANTITIES (e.g., MULTIPLES or RATIOS) to be retrieved or calculated,
the concrete results MUST CONTAIN SPECIFIC VALUES for such quantities for the answer to be considered confident.

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
