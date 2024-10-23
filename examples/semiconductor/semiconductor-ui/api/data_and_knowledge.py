from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from dotenv import load_dotenv
import yaml

if TYPE_CHECKING:
    from openssa.core.programming.hierarchical.plan import HTPDict


load_dotenv()


EXPERT_KNOWLEDGE_FILE_PATH: Path = Path(__file__).parent / 'expert-knowledge.txt'
with open(file=EXPERT_KNOWLEDGE_FILE_PATH,
          buffering=-1,
          encoding='utf-8',
          errors='strict',
          newline=None,
          closefd=True,
          opener=None) as f:
    EXPERT_KNOWLEDGE: str = f.read()


EXPERT_PROGRAM_SPACE_FILE_PATH: Path = Path(__file__).parent / 'expert-program-space.yml'
with open(file=EXPERT_PROGRAM_SPACE_FILE_PATH,
          buffering=-1,
          encoding='utf-8',
          errors='strict',
          newline=None,
          closefd=True,
          opener=None) as f:
    EXPERT_PROGRAM_SPACE: dict[str, HTPDict] = yaml.safe_load(stream=f)
