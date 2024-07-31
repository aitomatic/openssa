from openssa.core.inferencer.abstract_inferencer import AbstractInferencer
from openssa.core.slm.abstract_slm import AbstractSLM
from openssa.core.ssm.abstract_ssm import AbstractSSM
from openssa.core.ssm.abstract_ssm_builder import AbstractSSMBuilder
from openssa.core.ssm.base_ssm import BaseSSM


class BaseSSMBuilder(AbstractSSMBuilder):
    def __init__(self, initial_ssm: AbstractSSM = None):
        self._ssm = initial_ssm

    @property
    def ssm(self) -> AbstractSSM:
        if self._ssm is None:
            self._ssm = BaseSSM()
        return self._ssm

    @ssm.setter
    def ssm(self, ssm: AbstractSSM):
        self._ssm = ssm

    def add_knowledge(self, knowledge_source_uri: str, source_type=None):
        """Uploads a knowledge source (documents, text, files, etc.)"""
        pass

    def extract_structured_information(self, knowledge_id) -> list[str]:
        """Extracts structured information (facts, heuristics) from a specific knowledge source"""
        return []

    def add_inferencer(self, inferencer: AbstractInferencer, knowledge_id):
        """Adds or creates an inferencer (e.g., ML models) to a specific knowledge source"""
        pass

    def generate_training_data(self, knowledge_id, prompt_parameters=None) -> list[str]:
        """Generates instruction-following prompts from a specific knowledge source for fine-tuning a generic large model"""
        return []

    def train_slm(self, model, training_data, fine_tuning_parameters=None) -> AbstractSLM:
        """
        Fine-tunes a model based on the provided training data and fine-tuning parameters.
        Distills a large model into a smaller model based on the provided distillation parameters.
        """
        return self.ssm.slm

    def create_ssm(self, knowledge_ids, model_parameters=None) -> AbstractSSM:
        """Creates an SSM based on the provided knowledge sources and model parameters"""
        return self.ssm
