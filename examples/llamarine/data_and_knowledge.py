from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from dotenv import load_dotenv
import yaml

if TYPE_CHECKING:
    from openssa.core.programming.hierarchical.plan import HTPDict


load_dotenv()


EXPERT_KNOWLEDGE_PATH: Path = Path(__file__).parent / 'expert-knowledge.txt'
with open(file=EXPERT_KNOWLEDGE_PATH,
          buffering=-1,
          encoding='utf-8',
          errors='strict',
          newline=None,
          closefd=True,
          opener=None) as f:
    EXPERT_KNOWLEDGE: str = f.read()


EXPERT_PROGRAMS_PATH: Path = Path(__file__).parent / 'expert-programs.yml'
with open(file=EXPERT_PROGRAMS_PATH,
          buffering=-1,
          encoding='utf-8',
          errors='strict',
          newline=None,
          closefd=True,
          opener=None) as f:
    EXPERT_PROGRAMS: dict[str, HTPDict] = yaml.safe_load(stream=f)
