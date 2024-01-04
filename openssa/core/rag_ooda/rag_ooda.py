from llama_index.core import BaseRetriever  # noqa: TCH002
from llama_index.schema import NodeWithScore  # noqa: TCH002
from openssa.core.ooda_rag.builtin_agents import ContextValidator, SynthesizingAgent
from openssa.core.ssa.agent import Agent
from openssa.core.ooda_rag.tools import ResearchQueryEngineTool
from openssa.core.rag_ooda.resources.rag_resource import RagResource
from openssa.core.ooda_rag.ooda_rag import Solver


class RagOODA:
    def __init__(
        self, resources: list[RagResource] = None, conversation: list = None
    ) -> None:
        self.resources = resources or []
        self.conversation = conversation or []

    def retrieve_context(self, query) -> list:
        context = []
        for resource in self.resources:
            retriever: BaseRetriever = resource.retriever
            nodes: NodeWithScore = retriever.retrieve(query)
            context += [n.text for n in nodes]
        return context

    def is_sufficient(self, query: str, context: list) -> bool:
        context_validator = ContextValidator(
            conversation=self.conversation, context=context
        )
        return context_validator.execute(query).get("is_sufficient", False)

    def get_answer(self, query: str, context: list) -> str:
        synthesizer = SynthesizingAgent(conversation=self.conversation, context=context)
        return synthesizer.execute(query).get("answer", "")

    def chat(self, query: str) -> str:
        self.conversation.append({"role": "user", "content": query})
        context = self.retrieve_context(query)
        if self.is_sufficient(query, context):
            answer = self.get_answer(query, context)
            self.conversation.append({"role": "assistant", "content": answer})
        else:
            print("\nThe context is not sufficient. Starting OODA process\n")
            answer = self.ooda_a_solve(query, context)
        # self.conversation.append({"role": "assistant", "content": answer})
        return answer

    def ooda_a_solve(self, query: str, context: list) -> str:
        research_tool = ResearchQueryEngineTool(
            query_engine=self.resources[0].query_engine
        )
        # research_tool = ResearchDocumentsTool(agent_id="136")
        solver = Solver(
            enable_generative=True,
            conversation=self.conversation,
        )
        assistant_response = solver.run(query, {"research_documents": research_tool})
        return assistant_response

    def ooda_solve(self, query: str, context: list) -> str:
        agent = Agent()
        result = agent.solve(query)
        # return result.get("response", "")
        return result
