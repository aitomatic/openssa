from unittest.mock import Mock
from openssm.core.adapter.base_adapter import BaseAdapter
from openssm.core.backend.base_backend import BaseBackend


class MockBackend(BaseBackend):
    # we don't call any methods from AbstractBackend, we don't need to define
    # any in our mock
    pass


def test_get_backends():
    backends = [MockBackend(), MockBackend()]
    adapter = BaseAdapter(backends)
    assert adapter.get_backends() == backends


def test_add_backend():
    backend1 = MockBackend()
    backend2 = MockBackend()
    adapter = BaseAdapter([backend1])
    adapter.add_backend(backend2)
    assert adapter.get_backends() == [backend1, backend2]


def test_set_backends():
    backends1 = [MockBackend()]
    backends2 = [MockBackend(), MockBackend()]
    adapter = BaseAdapter(backends1)
    adapter.set_backends(backends2)
    assert adapter.get_backends() == backends2


def test_list_facts():
    adapter = BaseAdapter()
    adapter.list_facts = Mock()
    adapter.list_facts()
    adapter.list_facts.assert_called()


def test_list_inferencers():
    adapter = BaseAdapter()
    adapter.list_inferencers = Mock()
    adapter.list_inferencers()
    adapter.list_inferencers.assert_called()


def test_list_heuristics():
    adapter = BaseAdapter()
    adapter.list_heuristics = Mock()
    adapter.list_heuristics()
    adapter.list_heuristics.assert_called()


def test_select_facts():
    adapter = BaseAdapter()
    adapter.select_facts = Mock()
    adapter.select_facts({"mock_criteria": "mock_value"})
    adapter.select_facts.assert_called_with({"mock_criteria": "mock_value"})


def test_select_inferencers():
    adapter = BaseAdapter()
    adapter.select_inferencers = Mock()
    adapter.select_inferencers({"mock_criteria": "mock_value"})
    adapter.select_inferencers.assert_called_with(
        {"mock_criteria": "mock_value"})


def test_select_heuristics():
    adapter = BaseAdapter()
    adapter.select_heuristics = Mock()
    adapter.select_heuristics({"mock_criteria": "mock_value"})
    adapter.select_heuristics.assert_called_with(
        {"mock_criteria": "mock_value"})
