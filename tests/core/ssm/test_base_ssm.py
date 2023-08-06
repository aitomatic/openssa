from unittest.mock import MagicMock
import pytest
from openssm.core.slm.base_slm import BaseSLM
from openssm.core.ssm.base_ssm import BaseSSM
from openssm.core.adapter.base_adapter import BaseAdapter
from openssm.core.backend.base_backend import BaseBackend


# Mocking the dependencies
class MockSLM(BaseSLM):
    # pylint: disable=unused-argument
    def discuss(self, user_input: list[dict], conversation_id: str = None) -> list[dict]:
        return "Mock discuss response"

    def reset_memory(self):
        pass


class MockAdapter(BaseAdapter):
    def api_call(self, function_name, *args, **kwargs):
        assert function_name is not None
        assert args is not None
        assert kwargs is not None
        return "Mock api_call response"

    @property
    def facts(self):
        return ["Fact 1", "Fact 2"]

    @property
    def inferencers(self):
        return ["Inferencer 1", "Inferencer 2"]

    @property
    def heuristics(self):
        return ["Heuristic 1", "Heuristic 2"]

    def select_facts(self, criteria):
        assert criteria is not None
        return ["Fact 1"]

    def select_inferencers(self, criteria):
        assert criteria is not None
        return ["Inferencer 1"]

    def select_heuristics(self, criteria):
        assert criteria is not None
        return ["Heuristic 1"]

    def infer(self, criteria):
        assert criteria is not None
        return ["Inference Result"]


class MockBackend(BaseBackend):
    def dbprocess(self, conversation_id, user_input):
        assert conversation_id is not None
        assert user_input is not None
        return "Mock process response"


# Test setup
@pytest.fixture(autouse=True)
def setup_function():
    pytest.slm = MockSLM()
    pytest.adapter = MockAdapter()
    pytest.backends = [MockBackend(), MockBackend()]


# Test cases
def test_slm():
    ssm = BaseSSM(pytest.slm)
    assert ssm.slm == pytest.slm


def test_adapter():
    ssm = BaseSSM(pytest.slm, pytest.adapter)
    assert ssm.adapter == pytest.adapter


def test_backends():
    ssm = BaseSSM(pytest.slm, pytest.adapter, pytest.backends)
    assert ssm.backends == pytest.backends


def test_discuss():
    ssm = BaseSSM(pytest.slm)
    assert ssm.discuss("conversation_1", "Hello") == [{"role": "assistant", "content": "Mock discuss response"}]


def test_reset_memory():
    # We're using MagicMock here to be able to use .assert_called()
    pytest.slm.reset_memory = MagicMock()
    ssm = BaseSSM(pytest.slm)
    ssm.reset_memory()
    # Check that reset_memory was called on the slm
    pytest.slm.reset_memory.assert_called()


def test_list_facts():
    ssm = BaseSSM(pytest.slm, pytest.adapter)
    assert ssm.facts == ["Fact 1", "Fact 2"]


def test_list_inferencers():
    ssm = BaseSSM(pytest.slm, pytest.adapter)
    assert ssm.inferencers == ["Inferencer 1", "Inferencer 2"]


def test_list_heuristics():
    ssm = BaseSSM(pytest.slm, pytest.adapter)
    assert ssm.heuristics == ["Heuristic 1", "Heuristic 2"]


def test_select_facts():
    ssm = BaseSSM(pytest.slm, pytest.adapter)
    assert ssm.select_facts({"mock_criteria": "mock_value"}) == ["Fact 1"]


def test_select_inferencers():
    ssm = BaseSSM(pytest.slm, pytest.adapter)
    assert ssm.select_inferencers(
        {"mock_criteria": "mock_value"}) == ["Inferencer 1"]


def test_select_heuristics():
    ssm = BaseSSM(pytest.slm, pytest.adapter)
    assert ssm.select_heuristics(
        {"mock_criteria": "mock_value"}) == ["Heuristic 1"]


def test_infer():
    ssm = BaseSSM(pytest.slm, pytest.adapter)
    assert ssm.infer({"mock_criteria": "mock_value"}) == ["Inference Result"]


def test_solve_problem():
    ssm = BaseSSM()
    problem_description = ["Problem 1"]
    ssm.solve_problem = MagicMock(return_value=["Solution to Problem 1"])
    assert ssm.solve_problem(problem_description) == ["Solution to Problem 1"]
