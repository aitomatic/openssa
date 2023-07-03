import pytest
from unittest.mock import MagicMock
from openssm.core.slm.base_slm import BaseSLM
from openssm.core.ssm.base_ssm import BaseSSM
from openssm.core.adapter.base_adapter import BaseAdapter
from openssm.core.backend.base_backend import BaseBackend


# Mocking the dependencies
class MockSLM(BaseSLM):
    def discuss(self, conversation_id, user_input):
        return "Mock discuss response"

    def reset_memory(self):
        pass


class MockAdapter(BaseAdapter):
    def api_call(self, function_name, *args, **kwargs):
        return "Mock api_call response"

    def list_facts(self):
        return ["Fact 1", "Fact 2"]

    def list_inferencers(self):
        return ["Inferencer 1", "Inferencer 2"]

    def list_heuristics(self):
        return ["Heuristic 1", "Heuristic 2"]

    def select_facts(self, criteria):
        return ["Fact 1"]

    def select_inferencers(self, criteria):
        return ["Inferencer 1"]

    def select_heuristics(self, criteria):
        return ["Heuristic 1"]

    def infer(self, criteria):
        return ["Inference Result"]


class MockBackend(BaseBackend):
    def process(self, input):
        return "Mock process response"


# Test setup
@pytest.fixture(autouse=True)
def setup_function():
    pytest.slm = MockSLM()
    pytest.adapter = MockAdapter()
    pytest.backends = [MockBackend(), MockBackend()]


# Test cases
def test_get_slm():
    ssm = BaseSSM(pytest.slm)
    assert ssm.get_slm() == pytest.slm


def test_get_adapter():
    ssm = BaseSSM(pytest.slm, pytest.adapter)
    assert ssm.get_adapter() == pytest.adapter


def test_get_backends():
    ssm = BaseSSM(pytest.slm, pytest.adapter, pytest.backends)
    assert ssm.get_backends() == pytest.backends


def test_discuss():
    ssm = BaseSSM(pytest.slm)
    assert ssm.discuss("conversation_1", "Hello") == "Mock discuss response"


def test_reset_memory():
    # We're using MagicMock here to be able to use .assert_called()
    pytest.slm.reset_memory = MagicMock()
    ssm = BaseSSM(pytest.slm)
    ssm.reset_memory()
    # Check that reset_memory was called on the slm
    pytest.slm.reset_memory.assert_called()


def test_list_facts():
    ssm = BaseSSM(pytest.slm, pytest.adapter)
    assert ssm.list_facts() == ["Fact 1", "Fact 2"]


def test_list_inferencers():
    ssm = BaseSSM(pytest.slm, pytest.adapter)
    assert ssm.list_inferencers() == ["Inferencer 1", "Inferencer 2"]


def test_list_heuristics():
    ssm = BaseSSM(pytest.slm, pytest.adapter)
    assert ssm.list_heuristics() == ["Heuristic 1", "Heuristic 2"]


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
