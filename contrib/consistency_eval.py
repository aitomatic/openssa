from typing import Callable, Any, List
import os
from dotenv import load_dotenv
from openssa.core.util.lm.openai import OpenAILM
from openssa.core.util.lm.config import LMConfig

load_dotenv(dotenv_path="../examples/FinanceBench/.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ConsistencyScore:
    def __init__(self) -> None:
        """
        Initializes the ConsistencyScore class.
        """
        # Reading the content of the text file into a string
        file_path = './consistency_prompt.txt'
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        self.prompt_template = f"{file_content}"

        self.llm = OpenAILM.from_defaults()

    def specificity_score(self, question: str, output1: str, output2: str) -> int:
        """
        Placeholder for the specificity_score function.

        Args:
            output1 (Any): The first output from the LLM.
            output2 (Any): The second output from the LLM.

        Returns:
            float: The specificity score between the two outputs.
        """
        # Replace this with the actual implementation of the specificity_score function
        prompt = self.prompt_template + f"\n Question: {question} \n  String 1: {output1} \n String 2: {output2} \n Output:"
        eval_response = self.llm.get_response(prompt=prompt,
                                              history=None,
                                              json_format=bool)  
        
        # print(type(eval_response['output']))
        
        # return eval_response
        
        try:
            return int(eval_response['output'])
        except ValueError as ve:
            raise ValueError(f"Invalid eval_response value: {eval_response}. Expected '0' or '1'.") from ve

    def compute(self, prompt: str, num_tries: int, llm_inference_func: Callable[..., Any], inference_args: dict = None) -> List[float]:
        """
        Computes the consistency score by prompting the LLM multiple times and calculating the specificity score for each pair of outputs.

        Args:
            llm_inference_func (Callable[..., Any]): The LLM inference function.
            inference_args (dict): The arguments for the LLM inference function.
            prompt (str): The prompt to be used as input to the LLM.
            num_tries (int): The number of times to prompt the LLM.

        Returns:
            List[float]: A list of specificity scores for each pair of outputs.
        """
        if inference_args is None:
            inference_args = {}

        # Generate the outputs from the LLM
        outputs = [llm_inference_func(prompt, **inference_args) for _ in range(num_tries)]
        # outputs = [llm_inference_func(prompt, history=None, json_format=False) for _ in range(num_tries)]

        # Calculate specificity scores for each possible pair of outputs
        scores = []
        for i, output1 in enumerate(outputs):
            for j, output2 in enumerate(outputs):
                if j > i:
                    score = self.specificity_score(prompt, output1, output2)
                    scores.append(score)

        return sum(scores) / len(scores)  
        # return scores

def test():
    # inference_func = OpenAILM.from_defaults().get_response

    # prompt = "What is the capital of France?"
    # # num_tries = 4
    # # consistency_metric = ConsistencyScore()
    # # consistency_score = consistency_metric.compute(prompt=prompt, llm_inference_func=inference_func, num_tries=num_tries, inference_args={'history': None, 'json_format': False, 'response_format': { "type": "json_object"}})
    # # print(consistency_score)

    func = OpenAILM.from_defaults().get_response
    d = {'history': None, 'json_format': False}
    # r = func(prompt, **d)
    # print(r)

    prompt = "What is the capital of France?"
    num_tries = 4
    consistency_metric = ConsistencyScore()
    s = consistency_metric.compute(prompt=prompt, num_tries=num_tries, llm_inference_func=func, inference_args=d)
    print(s)
    # Example usage:
    # llm_inference_func = some_llm_function
    # inference_args = {'arg1': value1, 'arg2': value2}
    # prompt = "Your prompt here"
    # num_tries = 5
    # consistency = ConsistencyScore()
    # scores = consistency.compute(llm_inference_func, inference_args, prompt, num_tries)
    # print(scores)


if __name__ == "__main__":
    test()
