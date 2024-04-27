ORIENT_PROMPT_TEMPLATE: str = \
"""Assuming that the following question/problem/task is posed

```
{question}
```

and you have observed various answers/solutions from different informational resources as detailed below,
please evaluate whether you can answer/solve the posed question/problem/task confidently with concrete results.
If the question/problem/task mentions any RIGOROUS BASES/CRITERIA/DEFINITIONS for judgement,
the concrete results MUST RESPOND TO SUCH BASES/CRITERIA/DEFINITIONS for the answer/solution to be considered confident.
If the question/problem/task involves any NUMERICAL QUANTITIES (e.g., MULTIPLES or RATIOS) to be retrieved or calculated,
the concrete results MUST CONTAIN SPECIFIC VALUES for such quantities for the answer/solution to be considered confident.

If you can answer/solve confidently with concrete results, return a JSON dictionary
`{{"confident": true,
   "answer": "<confident answer/solution of up to {n_words:,} words, covering reasoning flow and supporting details>"}}`.

If you cannot answer/solve confidently with concrete results, return a JSON dictionary
`{{"confident": false,
   "answer": "<best-effort answer/solution of up to {n_words:,} words, covering potentially useful supporting details>"}}`.

Please return ONLY the JSON DICTIONARY and no other text, not even the "```json" wrapping!


```
{observations}
```
"""  # noqa: E122
