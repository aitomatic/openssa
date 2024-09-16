from pathlib import Path
import sys

from openssa import FileResource, __path__

FINANCE_BENCH_DIR_PATH: Path = Path(__path__[0]).parent / 'examples' / 'FinanceBench'
sys.path.append(str(FINANCE_BENCH_DIR_PATH))

# pylint: disable=wrong-import-order,wrong-import-position
from rag import get_or_create_file_resource  # noqa: E402


def test_file_resource():
    file_resource: FileResource = get_or_create_file_resource(doc_name='AMD_2022_10K')
    answer: str = file_resource.answer(question="What is the company's latest annual revenue?")
    assert isinstance(answer, str)
