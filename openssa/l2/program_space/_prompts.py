PROGRAM_SEARCH_PROMPT_TEMPLATE: str = (
"""Consider that you can access informational resources summarized in the below dictionary,
in which each key is a resource's unique name and the corresponding value is that resource's overview:

```
{resource_overviews}
```

and consider that you are trying to solve the following question/problem/task:

```
{problem}
```

and that you have access to a collection of problem-solving programs
summarized by the below name-description pairs:

```
{program_descriptions}
```

Please return the name of the most appropriate program for solving the posed question/problem/task,
ONLY IF at least one program is deemed applicable/suitable.

Otherwise, if no applicable/suitable programs are found in the collection,
please return the word NONE.

*** STRICTLY return either a precise program name or the word NONE, with no surrounding quotation characters ***
"""  # noqa: E122
)
