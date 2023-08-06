# pylint: disable=too-few-public-methods
class Prompts:
    _PROMPTS = {"openssm": {"core": {
        "slm": {
            "base_slm": {
                "completion":
                    "Complete this conversation with the assistant’s response, up to 2000 words. "
                    "Use this format: {\"role\": \"assistant\", \"content\": \"xxx\"}, "
                    "where 'xxx' is the response. "
                    "Make sure the entire response is valid JSON, xxx is only a string, "
                    "and no code of any kind, even if the prompt has code. "
                    "Escape quotes with \\:\n"
            }
        },
        "ssm": {
            "rag_ssm": {
                "_combine_inputs":
                    "Answer the following (Question), by combining your own knowledge "
                    "with that provided by a document-backed model (RAG), taking into account "
                    "the fact that both you and the RAG model are imperfect, with possible "
                    "hallucination. Do the best you can. "
                    "Question: {user_input} "
                    "RAG: {rag_response}"
            }
        }
    }}}

    @staticmethod
    def get_module_prompt(module_name: str, *subindices: str) -> dict:
        keys = module_name.split('.')
        if subindices:
            keys.extend(subindices)

        value = Prompts._PROMPTS
        for key in keys:
            value = value.get(key, {})

        if value == {}:
            raise ValueError("Could not find prompt for module_name={module_name}, subindices={subindices}")

        return value
