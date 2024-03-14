import asyncio
import os
from typing import List

from dotenv import load_dotenv
from evaluate import load
from llama_index.core.evaluation import CorrectnessEvaluator, SemanticSimilarityEvaluator

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class Evaluator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.bert_evaluator = load("bertscore")
        self.cosine_evaluator = SemanticSimilarityEvaluator()
        self.correctness_evaluator = CorrectnessEvaluator()

    def evaluate(self, questions: List[str], answers: List[str], ground_truths: List[str]):
        f1 = self.f1_scores(answers, ground_truths)
        cosine = self.cosine_scores(answers, ground_truths)
        correctness = self.correctness_scores(questions, answers, ground_truths)
        print(f"\n -------- Evaluation results --------")
        print(f"F1 scores: {f1}")
        print(f"Cosine scores: {cosine}")
        print(f"Correctness scores: {correctness}")

    def f1_scores(self, answers: List[str], ground_truths: List[str]):
        """Calculate BERT's embedding-based similarity."""
        scores = self.bert_evaluator.compute(
            predictions=answers, references=ground_truths, lang="en"
        )
        return scores["f1"]

    def cosine_scores(self, answers: List[str], ground_truths: List[str]):
        """Calculate Ada's embedding-based similarity."""
        return asyncio.run(self.acosine_scores(answers, ground_truths))

    def correctness_scores(
        self, questions: List[str], answers: List[str], ground_truths: List[str]
    ):
        """Calculate correctness scores."""
        return asyncio.run(self.acorrectness_scores(questions, answers, ground_truths))

    async def acosine_scores(self, answers: List[str], ground_truths: List[str]):
        results = await asyncio.gather(
            *[
                self.cosine_evaluator.aevaluate(response=answer, reference=ground_truth)
                for answer, ground_truth in zip(answers, ground_truths)
            ]
        )
        scores = [result.score for result in results]
        return scores

    async def acorrectness_scores(
        self, questions: List[str], answers: List[str], ground_truths: List[str]
    ):
        results = await asyncio.gather(
            *[
                self.correctness_evaluator.aevaluate(
                    query=question, response=answer, reference=ground_truth
                )
                for question, answer, ground_truth in zip(questions, answers, ground_truths)
            ]
        )
        scores = [result.score for result in results]
        return scores


if __name__ == "__main__":
    questions = [
        "What is the capital of Vietnam?",
        "What is the capital of Vietnam?",
        "What is the capital of Vietnam?",
    ]
    answers = [
        "The capital of Vietnam is Ho Chi Minh City.",
        "The capital of Vietnam is Ho Chi Minh City.",
        "The capital of Vietnam is Ho Chi Minh City.",
    ]
    ground_truths = [
        "The capital of Vietnam is Ho Chi Minh City.",
        "The capital of Vietnam is Bangkok.",
        "I had lunch at Pho Ha in Saigon.",
    ]
    Evaluator(api_key=OPENAI_API_KEY).evaluate(questions, answers, ground_truths)
