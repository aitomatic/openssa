PROGRAM_SEARCH_PROMPT_TEMPLATE: str = (
"""
Consider that you are trying to solve the following question/problem/task:

```
{problem}
```

and that you have access to a collection of executable solution programs
summarized by the below name-description pairs:

```json
{program_descriptions}
```

Please return the name of the most appropriate program for solving the stated question/problem/task,
ONLY IF at least one program is deemed applicable/relevant.

Otherwise, if no applicable/relevant programs are found in the collection,
please return the word NONE.
"""  # noqa: E122
)
