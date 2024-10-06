from functools import cache
from pathlib import Path


DATA_LOCAL_DIR_PATH: Path = Path(__file__).parent / '.data'


@cache
def get_or_create_cached_dir_path(company: str) -> str:
    dir_path: Path = DATA_LOCAL_DIR_PATH / company
    dir_path.mkdir(parents=True, exist_ok=True)
    return str(dir_path)
