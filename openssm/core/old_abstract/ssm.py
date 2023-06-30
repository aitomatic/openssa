"""Abstract SSM."""


from dataclasses import dataclass
from llama_index import VectorStoreIndex
from llama_hub.file.base import SimpleDirectoryReader
from langchain.llms.base import LLM


@dataclass
class KnowledgeSet:
    """Abstract Knowledge Set."""

    storage: str   # file path for now
    # lang_model_connector: SimpleDirectoryReader


@dataclass
class FactSet(KnowledgeSet):
    """Collection of Facts."""


@dataclass
class InferRuleSet(KnowledgeSet):
    """Collection of Inference Rules."""


class SSM:
    def __init__(self,
                 name: str,
                 description: str,
                 communicator: LLM,
                 fact_sets: set[FactSet],
                 infer_rule_sets: set[InferRuleSet]):
        self.name = name
        self.description = description
        self.communicator = communicator
        self.fact_sets = fact_sets
        self.infer_rule_sets = infer_rule_sets

        self.load_knowledge()

    def load_knowledge(self):
        for fact_set in self.fact_sets:
            loader = SimpleDirectoryReader(fact_set.storage,
                                           recursive=True,
                                           exclude_hidden=True)
            documents = loader.load_data()
            self.facts_index = VectorStoreIndex.from_documents(documents)
            print('Facts loaded.')

        for infer_rule_set in self.infer_rule_sets:
            loader = SimpleDirectoryReader(infer_rule_set.storage,
                                           recursive=True,
                                           exclude_hidden=True)
            documents = loader.load_data()
            self.infer_rules_index = VectorStoreIndex.from_documents(documents)
            print('Inference Rules loaded.')

    def process_request(self, request: str):
        return self.chat(request)

    def chat(self, request: str):
        return self.facts_index.as_chat_engine().chat(request)  # TODO: complex

    def infer(self, request: str):
        ...
