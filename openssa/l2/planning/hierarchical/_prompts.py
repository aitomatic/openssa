HTP_JSON_TEMPLATE: str = """
{{
    "task": "(textual description of problem/task to solve)",
    "sub-plans": [
        {{
            "task": "(textual description of 1st sub-problem/sub-task to solve)",
            "sub-plans": [
                (... nested sub-plans ...)
            ]
        }},
        {{
            "task": "(textual description of 2nd sub-problem/sub-task to solve)",
            "sub-plans": [
                (... nested sub-plans ...)
            ]
        }},
        ...
    ]
}}
"""

HTP_WITH_RESOURCES_JSON_TEMPLATE: str = """
{{
    "task": {{
        "ask": "(textual description of problem/task to solve)"
    }},
    "sub-plans": [
        {{
            "task": {{
                "ask": "(textual description of 1st sub-problem/sub-task to solve)",
                "resource": "(unique name of most relevant informational resource, IF ANY)" OR null
            }},
            "sub-plans": [
                (... nested sub-plans ...)
            ]
        }},
        {{
            "task": {{
                "ask": "(textual description of 2nd sub-problem/sub-task to solve)",
                "resource": "(unique name of most relevant informational resource, IF ANY)" OR null
            }},
            "sub-plans": [
                (... nested sub-plans ...)
            ]
        }},
        ...
    ]
}}
"""


def htp_prompt_template(with_resources: bool) -> str:
    return (
'Using the following JSON hierarchical task plan data structure:'  # noqa: E122
f'\n{HTP_WITH_RESOURCES_JSON_TEMPLATE if with_resources else HTP_JSON_TEMPLATE}'  # noqa: E122
"""
please return a suggested hierarchical task plan with
Max Depth of {max_depth} and Max Subtasks per Decomposition of {max_subtasks_per_decomp}
for the following problem:

```
{problem}
```

Please return ONLY the JSON DICTIONARY and no other text, not even the "```json" wrapping!
"""  # noqa: E122
)  # noqa: E122


HTP_PROMPT_TEMPLATE: str = htp_prompt_template(with_resources=False)


RESOURCE_OVERVIEW_PROMPT_SECTION: str = \
"""Consider that you can access informational resources summarized in the below dictionary,
in which each key is a resource's unique name and the corresponding value is that resource's overview:

```
{resource_overviews}
```

"""  # noqa: E122


HTP_WITH_RESOURCES_PROMPT_TEMPLATE: str = RESOURCE_OVERVIEW_PROMPT_SECTION + htp_prompt_template(with_resources=True)


HTP_UPDATE_RESOURCES_PROMPT_TEMPLATE: str = (
RESOURCE_OVERVIEW_PROMPT_SECTION +  # noqa: E122
"""please return an updated version of the following JSON hierarchical task plan
by appropriately replacing `"resource": null` with `"resource": "(unique name of most relevant informational resource)"`
for any case in which such a relevant informational resource can be identified for the corresponding problem/task:

```json
{htp_json}
```

Please return ONLY the UPDATED JSON DICTIONARY and no other text, not even the "```json" wrapping!
"""  # noqa: E122
)


HTP_RESULTS_SYNTH_PROMPT_TEMPLATE: str = (
"""Synthesize an answer/solution for the following question/problem/task:

```
{ask}
```

given the following collection of reasoning and results:

```
{info}
```
"""  # noqa: E122
)
