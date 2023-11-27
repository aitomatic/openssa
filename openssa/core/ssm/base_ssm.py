import os
import uuid
from openssa.core.ssm.abstract_ssm import AbstractSSM
from openssa.core.slm.abstract_slm import AbstractSLM
from openssa.core.adapter.abstract_adapter import AbstractAdapter
from openssa.core.backend.abstract_backend import AbstractBackend
from openssa.core.slm.base_slm import BaseSLM
from openssa.core.adapter.base_adapter import BaseAdapter
from openssa.core.backend.base_backend import BaseBackend
from openssa.utils.utils import Utils
from openssa.utils.logs import Logs


# pylint: disable=too-many-public-methods
class BaseSSM(AbstractSSM):
    DEFAULT_CONVERSATION_ID = str(uuid.uuid4())[:4]

    # pylint: disable=too-many-arguments
    def __init__(self,
                 slm: AbstractSLM = None,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None,
                 name: str = None,
                 storage_dir: str = None):
        self._slm = slm
        self.slm.adapter = adapter
        self.adapter.backends = backends
        self._name = name
        self._storage_dir = storage_dir
        self._conversation_tracking = True
        self._conversations = {}

    @property
    def conversation_tracking(self) -> bool:
        """
        Return the previous assigned track_conversations,
        or True if none was assigned.
        """
        if self._conversation_tracking is None:
            self._conversation_tracking = True
        return self._conversation_tracking

    @conversation_tracking.setter
    def conversation_tracking(self, track_conversations: bool):
        """
        Set the track_conversations flag.
        """
        self._conversation_tracking = track_conversations

    @property
    def conversations(self) -> dict:
        """
        Return the previous assigned conversations,
        or an empty dictionary if none was assigned.
        """
        if self._conversations is None:
            self._conversations = {}
        return self._conversations

    @conversations.setter
    def conversations(self, conversations: dict):
        self._conversations = conversations

    @property
    def slm(self) -> AbstractSLM:
        """
        Return the previous assigned SLM,
        or a default SLM if none was assigned.
        """
        if self._slm is None:
            self._slm = BaseSLM()
        return self._slm

    @slm.setter
    def slm(self, slm: AbstractSLM):
        self._slm = slm

    @property
    def adapter(self) -> AbstractAdapter:
        """
        Return the previous assigned Adapter,
        or a default Adapter if none was assigned.
        """
        if self.slm.adapter is None:
            self.slm.adapter = BaseAdapter()
        return self.slm.adapter

    @adapter.setter
    def adapter(self, adapter: AbstractAdapter):
        self.slm.adapter = adapter

    @property
    def backends(self) -> list[AbstractBackend]:
        """
        Return the previous assigned backends,
        or a default backend if none was assigned.
        """
        if self.adapter.backends is None:
            self.adapter.backends = [BaseBackend()]
        return self.adapter.backends

    @backends.setter
    def backends(self, backends: list[AbstractBackend]):
        self.adapter.backends = backends

    @property
    def name(self) -> str:
        """
        Return the previous assigned name,
        or a default name if none was assigned.
        """
        if self._name is None:
            self._name = f"ssm-{uuid.uuid4().hex[:8]}"
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    def get_conversation(self, conversation_id: str = None) -> list[dict]:
        """
        Return the conversation with the given id.
        Instantiate a new conversation if none was found, and an id was given.
        """
        if conversation_id is None:
            return []

        self.conversations[conversation_id] = self.conversations.get(conversation_id, [])
        return self.conversations[conversation_id]

    def api_call(self, function_name, *args, **kwargs):
        return self.adapter.api_call(function_name, *args, **kwargs)

    @property
    def facts(self) -> list[str]:
        """
        Return the facts from the adapter.
        """
        return self.adapter.facts

    @property
    def inferencers(self) -> list[str]:
        """
        Return the inferencers from the adapter.
        """
        return self.adapter.inferencers

    @property
    def heuristics(self) -> list[str]:
        """
        Return the heuristics from the adapter.
        """
        return self.adapter.heuristics

    def select_facts(self, criteria: dict) -> list[str]:
        return self.adapter.select_facts(criteria)

    def select_inferencers(self, criteria: dict) -> list[str]:
        return self.adapter.select_inferencers(criteria)

    def select_heuristics(self, criteria: dict) -> list[str]:
        return self.adapter.select_heuristics(criteria)

    def infer(self, input_facts: dict) -> list[str]:
        return self.adapter.infer(input_facts)

    def solve_problem(self, problem_description: list[str]) -> list[str]:
        pass

    def add_knowledge(self, knowledge_source_uri: str, knowledge_type=None):
        """Uploads a knowledge source (documents, text, files, etc.)"""
        # self.adapter.add_knowledge(knowledge_source_uri, knowledge_type)

    @property
    def storage_dir(self) -> str:
        if self._storage_dir is None:
            self._storage_dir = self._default_storage_dir
        return self._storage_dir

    @storage_dir.setter
    def storage_dir(self, storage_dir: str):
        self._storage_dir = storage_dir

    @property
    def _default_storage_dir(self) -> str:
        base_dir = os.environ.get("openssa_STORAGE_DIR", ".openssa")
        return os.path.join(base_dir, self.name)

    def save(self, storage_dir: str = None):
        """Saves the SSM to the specified directory."""
        self.storage_dir = storage_dir or self.storage_dir
        self.slm.save(self.storage_dir)
        self.adapter.save(self.storage_dir)
        self.adapter.enumerate_backends(lambda backend: backend.save(self.storage_dir))

    def load(self, storage_dir: str = None):
        """Loads the SSM from the specified directory."""
        self.storage_dir = storage_dir or self.storage_dir
        self.slm.load(self.storage_dir)
        self.adapter.load(self.storage_dir)
        self.adapter.enumerate_backends(lambda backend: backend.load(self.storage_dir))

    def update_conversation(self, user_input: list[dict], reply: dict, conversation_id: str = None) -> list[dict]:
        """
        Update the conversation with the user_input and reply.
        """
        conversation = self.get_conversation(conversation_id)

        if user_input is not None:
            conversation.extend(user_input)

        if reply is not None:
            conversation.append(reply)

    def custom_discuss(self, user_input: list[dict], conversation: list[dict]) -> tuple[dict, list[dict]]:
        """
        Send user input to our SLM and return the reply, AND the actual user input.
        In the base implementation, the user_input is unchanged from what we are given.
        But derived classes can override this method to do things like:

        - Add other context info to the user_input
        - Query other models first and combine their replies to form a single user_input
        - etc.
        """
        reply = self.slm.do_discuss(user_input, conversation)
        return reply, user_input

    @Utils.do_canonicalize_user_input_and_discuss_result('user_input')
    @Logs.do_log_entry_and_exit()
    def discuss(self, user_input: list[dict], conversation_id: str = None) -> dict:
        if self.conversation_tracking and conversation_id is None:
            conversation_id = self.DEFAULT_CONVERSATION_ID

        # Always retrieve the conversation first
        conversation = self.get_conversation(conversation_id)

        response, actual_input = self.custom_discuss(user_input, conversation)

        # Update the conversation
        if self.conversation_tracking:
            self.update_conversation(actual_input, response, conversation_id)

        return response

    def reset_memory(self):
        self.conversations = None
        self.slm.reset_memory()
        # adapters and backends are stateless so no need to reset them
