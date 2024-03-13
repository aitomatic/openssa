from typing import Union, ClassVar
from uuid import uuid4
from llama_index.core.retrievers import BaseRetriever  # noqa: TCH002
from llama_index.core.schema import NodeWithScore  # noqa: TCH002
from openssa.core.ooda_rag.builtin_agents import (
    ContextValidator,
    SynthesizingAgent,
    AnswerValidator,
    GoalAgent,
)
from openssa.core.ooda_rag.tools import (
    ResearchQueryEngineTool,
    Tool,
)
from openssa.core.rag_ooda.resources.rag_resource import RagResource
from openssa.core.ooda_rag.ooda_rag import Solver, Notifier, SimpleNotifier, EventTypes
from openssa.utils.utils import Utils


class RagOODA:
    _conversations: ClassVar[dict] = {}

    @classmethod
    def get_conversation(cls, conversation_id: str) -> list:
        return cls._conversations.get(conversation_id, [])

    @classmethod
    def set_conversation(cls, conversation_id: str, conversation: list) -> None:
        cls._conversations[conversation_id] = conversation

    def __init__(
        self,
        resources: list[Union[RagResource, Tool]] = None,
        conversation_id: str = str(uuid4()),
        notifier: Notifier = SimpleNotifier(),
    ) -> None:
        self.resources = resources or []
        self.conversation = RagOODA.get_conversation(conversation_id)
        if not self.conversation:
            self.conversation = [
                {"role": "assistant", "content": "Hello, how can I help you?"}
            ]
            RagOODA.set_conversation(conversation_id, self.conversation)
        self.notifier = notifier

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

    def is_answer_complete(self, query: str, answer: str) -> bool:
        return AnswerValidator(answer=answer).execute(query)

    @Utils.timeit
    def chat_with_agent(self, query: str) -> str:
        # use standard agent and check answer is sufficient from agent
        self.conversation.append({"role": "user", "content": query})
        problem_statement = GoalAgent(conversation=self.conversation).execute(query)
        problem_statement = problem_statement if problem_statement else query
        agent_tool: Tool = self.resources[0]
        answer = agent_tool.execute(problem_statement).get("content", "")
        if answer and self.is_answer_complete(problem_statement, answer):
            self.conversation.append({"role": "assistant", "content": answer})
        else:
            self.notifier.notify(
                EventTypes.SWICTH_MODE,
                "Agent couldn't find answer. Starting OODA process.",
            )
            answer = self.ooda_solve(problem_statement, agent_tool)
        self.conversation.append({"role": "assistant", "content": answer})
        return answer

    @Utils.timeit
    def chat(self, query: str) -> str:
        # use retriever and check context if sufficient from retriever
        self.conversation.append({"role": "user", "content": query})
        context = self.retrieve_context(query)
        if self.is_sufficient(query, context):
            answer = self.get_answer(query, context)
            self.conversation.append({"role": "assistant", "content": answer})
        else:
            self.notifier.notify(EventTypes.SWICTH_MODE, "Starting OODA process")
            query_tool = ResearchQueryEngineTool(
                query_engine=self.resources[0].query_engine
            )
            answer = self.ooda_solve(query, query_tool)
        self.conversation.append({"role": "assistant", "content": answer})
        return answer

    def ooda_solve(self, query: str, query_tool: Tool) -> str:
        # research_tool = ResearchDocumentsTool(agent_id="136")
        solver = Solver(
            enable_generative=True,
            conversation=self.conversation,
        )
        assistant_response = solver.run(query, {"research_documents": query_tool})
        return assistant_response
