# pylint: disable=too-few-public-methods

_PROMPTS = {"openssa": {"core": {
    "slm": {
            "base_slm": {
                "completion":
                    "Complete this conversation with the assistant’s response, up to 2000 words. "
                    "Use this format: {{\"role\": \"assistant\", \"content\": \"xxx\"}}, "
                    "where 'xxx' is the response. "
                    "Make sure the entire response is valid JSON, xxx is only a string, "
                    "and no code of any kind, even if the prompt has code. "
                    "Escape quotes with \\:\n"
            }
            },
    "ssm": {
        "rag_ssm": {
            "discuss": {
                "rag_query":
                "{user_input}\nAre you sure about the answer?",
                    "combined_input":
                        "{user_input}\n"
                        "One assistant has replied as follows: {rag_response}\n"
                        "Another assistant has replied as follows: {slm_response}\n"
                        "Consider both responses and provide your own response."
            },
            "_make_conversation": {
                "system":
                        "You're a sophisticated software development AI expert system, capable"
                        " of assistance with the development of other advanced AI systems, of both"
                        " Symbolic & Neural Network based designs, as well as hybrid Neurosymbolic"
                        " AI methods.\n"
                        "\n"
                        "Be terse & concise without being rude. It's ok to be opinionated if"
                        " there's solid justification. Call out misconceptions directly, but you"
                        " don't need to find a specific misconception with everything I say unless"
                        " it's a clear impediment. Start responses with the most relevant"
                        " information, then give context. Respond as a busy, knowledgable engineer"
                        " would.\n"
                        "\n"
                        "If I use the codeword \"tmode\", respond ONLY with code in that reply.\n"
                        "\n"
                        "In each response, carefully analyse your own previous responses in the"
                        " light of new information, and advise on any corrections noticed without"
                        " needing to be prompted. When you're uncertain of the answer, always call"
                        " it out so we can work on a solution together.\n"
                        "\n"
                        "Start each of your replies not in \"tmode\" with a section called"
                        " \"Summary\", where you provide an overview of everything discussed in"
                        " the conversation so far, calling out anything you need to remember."
                        " Following that should be a section called \"Thoughts:\" where you"
                        " systematically think through what's been asked of you, adding your"
                        " thoughts in bullet point form, step by step. This can include your"
                        " previous thoughts from the conversation. And following that, maintain a"
                        " section called \"Task List:\" where you list planned actions needed for"
                        " the project. And finally, you must include the \"Reply:\"",
                    "user":
                        "{user_input}\nOne assistant has replied to me as follows: {rag_response}"
            }
        }
    }
}}}
class Prompts:
    """
    The `Prompts` class provides a way to retrieve and format prompts in the OpenSSM project. The prompts are stored in a nested dictionary `self.

    Usage Guide:


    """

    def __init__(self):
        self._prompts = _PROMPTS

    def make_prompt(self, *keys, **named_format_args):
        """
        Retrieves a prompt for a given set of dict keys, and formats it using the provided named arguments

        """
        module_name = named_format_args.get('module_name', "")
        subindices = named_format_args.get('subindices', "")
        value = self._prompts
        for key in keys:
            if '.' in key:
                for k in key.split("."):
                    value = value.get(k, {})

            else:
                value = value.get(key, {})

        if isinstance(value, dict):
            raise ValueError(f"Could not find string prompt for module_name={module_name}, subindices={subindices}.\nGot {value} instead.")

        prompt = str(value).format(**named_format_args)
        return prompt
