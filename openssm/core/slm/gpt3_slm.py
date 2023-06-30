from .base_slm import BaseSLM
import openai

class GPT3SLM(BaseSLM):
    def __init__(self, adapter=None):
        super().__init__(adapter)

    def setup_prompt(self):
        self.prompt = {
            "role": "system",
            "content": """You are a sophisticated language model trained to translate human natural language queries into structured commands for API function calls to the Adapter. 

            Your objective is to process user input and map it to a structured command that includes the method name and necessary parameters for the corresponding Adapter layer method calls. Here are the key methods you might need:

            1. "list_facts": Retrieves all the facts known by the system. No parameters required.
            2. "select_facts": Selects and retrieves facts based on the provided criteria. Requires the 'criteria' parameter.
            3. "query_facts": Queries for specific facts based on the provided criteria. Requires the 'criteria' parameter.
            4. "query_inferences": Makes an inference or prediction based on the provided inputs. Requires the 'inputs' parameter.
            5. "query_heuristics": Provides a solution or approach to solve the specified problem based on known heuristics. Requires the 'problem' parameter.

            Please map user inquiries accurately to a structured command in the format: 
            {"method": "<method_name>", "params": {"<param_name>": "<param_value>", ...}}"""
        }

    def process(self, input_text):
        # Generate the assistant's message that includes the structured command
        assistant_message = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                self.prompt,
                {"role": "user", "content": input_text}
            ]
        )
        # The assistant's reply is expected to be a structured command
        structured_command = json.loads(assistant_message['choices'][0]['message']['content'])
        return structured_command

    def translate(self, structured_command):
        method = structured_command['method']
        params = structured_command['params']
        # Make function call using method and params
        result = getattr(self.adapter, method)(**params)
        return result
