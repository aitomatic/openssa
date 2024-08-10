HTP_JSON_TEMPLATE: str = """
{{
    "task": "(textual description of question/problem/task to answer/solve)",
    "sub-htps": [
        {{
            "task": "(textual description of 1st sub-question/problem/task to answer/solve)",
            "sub-htps": [
                (... nested sub hierarchical task plans (sub-HTPs) ...)
            ]
        }},
        {{
            "task": "(textual description of 2nd sub-question/problem/task to answer/solve)",
            "sub-htps": [
                (... nested sub hierarchical task plans (sub-HTPs) ...)
            ]
        }},
        ...
    ]
}}
"""

HTP_WITH_RESOURCES_JSON_TEMPLATE: str = """
{{
    "task": {{
        "ask": "(textual description of question/problem/task to answer/solve)"
    }},
    "sub-htps": [
        {{
            "task": {{
                "ask": "(textual description of 1st sub-question/problem/task to answer/solve)",
                "resources": [
                    (... unique names of most relevant informational resources, if any ...)
                ]
            }},
            "sub-htps": [
                (... nested sub hierarchical task plans (sub-HTPs) ...)
            ]
        }},
        {{
            "task": {{
                "ask": "(textual description of 2nd sub-question/problem/task to answer/solve)",
                "resources": [
                    (... unique names of most relevant informational resources, if any ...)
                ]
            }},
            "sub-htps": [
                (... nested sub hierarchical task plans (sub-HTPs) ...)
            ]
        }},
        ...
    ]
}}
"""


def htp_prompt_template(with_resources: bool) -> str:
    return (
'Using the following JSON hierarchical task plan dictionary data structure:'  # noqa: E122
f'\n{HTP_WITH_RESOURCES_JSON_TEMPLATE if with_resources else HTP_JSON_TEMPLATE}'  # noqa: E122
"""
please return a suggested hierarchical task plan with
Max Depth of {max_depth} and Max Subtasks per Decomposition of {max_subtasks_per_decomp}
for the following question/problem/task:

```
{problem}
```

Please return ONLY the JSON DICTIONARY and no other text, not even the "```json" wrapping!
"""  # noqa: E122
)  # noqa: E122


HTP_PROMPT_TEMPLATE: str = htp_prompt_template(with_resources=False)


RESOURCE_OVERVIEW_PROMPT_SECTION: str = \
"""Consider that you can access resources summarized in the below dictionary,
in which each key is a resource's unique name and the corresponding value is that resource's overview:

```
{resource_overviews}
```

"""  # noqa: E122


HTP_WITH_RESOURCES_PROMPT_TEMPLATE: str = RESOURCE_OVERVIEW_PROMPT_SECTION + htp_prompt_template(with_resources=True)


HTP_UPDATE_RESOURCES_PROMPT_TEMPLATE: str = (
RESOURCE_OVERVIEW_PROMPT_SECTION +  # noqa: E122
"""and consider that you are trying to solve the following top-level question/problem/task:

```
{problem}
```

please return an updated version of the following JSON hierarchical task plan
by appropriately replacing `"resources": null` or `"resources": []`
with `"resources": [(... unique names of most relevant informational resources ...)]`
for any case in which such relevant informational resource(s) can be identified
for the corresponding sub-question/problem/task:

```json
{htp_json}
```

Please return ONLY the UPDATED JSON DICTIONARY and no other text, not even the "```json" wrapping!
"""  # noqa: E122
)


SIMPLIFIED_DECOMPOSITION_PROMPT_TEMPLATE: str = (
RESOURCE_OVERVIEW_PROMPT_SECTION +  # noqa: E122
"""and consider that you are trying to solve the following top-level question/problem/task:

```
{problem}
```

please return a sequence of up to {max_subtasks_per_decomp} sentences/paragraphs,
EACH PREPENDED by a header "[SUB-QUESTION/PROBLEM/TASK]" (EXACTLY LITERALLY THAT STRING! DO NOT SUBSTITUTE THAT STRING!),
describing how such top-level question/problem/task could/should be decomposed into sub-questions/problems/tasks,
per the following template:

```
[SUB-QUESTION/PROBLEM/TASK]
<textual description of 1st sub-question/problem/task to answer/solve>
[SUB-QUESTION/PROBLEM/TASK]
<textual description of 1st sub-question/problem/task to answer/solve>
...
```

Please return ONLY the SEQUENCE OF SENTENCES/PARAGRAPHS WITH SUCH HEADERS, and no other text.
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

Please present important reasoning flows and supporting details, but
please DO NOT USE GENERIC NAMES/NUMBERS TO REFER TO SUPPORTING DETAILS
(e.g., "Supporting Question/Task #3", "Supporting Result #4", etc.)
because such generic referencing names could get very confusing when presented in larger conversations.
"""  # noqa: E122
)
