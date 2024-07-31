from abc import ABC, abstractmethod
from openssa.core.slm.abstract_slm import AbstractSLM
from openssa.core.ssm.abstract_ssm import AbstractSSM


class AbstractSSMBuilder(ABC):
    @abstractmethod
    def add_knowledge(self, knowledge_source_uri: str, source_type=None) -> str:
        """Uploads a knowledge source (documents, text, files, etc.), returning `knowledge_id`"""

    @abstractmethod
    def extract_structured_information(self, knowledge_id) -> list[str]:
        """Extracts structured information (facts, heuristics) from a specific `knowledge_id`"""

    @abstractmethod
    def add_inferencer(self, inferencer, knowledge_id):
        """Adds or creates an inferencer (e.g., ML models) to a specific knowledge source"""

    @abstractmethod
    def generate_training_data(self, knowledge_id, prompt_parameters=None) -> list[str]:
        """Generates instruction-following prompts from a specific knowledge source for fine-tuning a generic large model"""

    @abstractmethod
    def train_slm(self, model, training_data, fine_tuning_parameters=None) -> AbstractSLM:
        """
        Fine-tunes a model based on the provided training data and fine-tuning parameters.
        Distills a large model into a smaller model based on the provided distillation parameters.
        """

    @abstractmethod
    def create_ssm(self, knowledge_ids, model_parameters=None) -> AbstractSSM:
        """Creates an SSM based on the provided knowledge sources and model parameters"""
