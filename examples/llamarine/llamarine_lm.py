from __future__ import annotations

from argparse import ArgumentParser
from dataclasses import dataclass

from openssa.core.util.lm.llama import LlamaLM
import os


DEFAULT_MODEL = 'llamarine-navigation'
DEFAULT_API_KEY = ''
DEFAULT_API_BASE = 'https://rpuoashq-llamarine-navigation-inference.tin.lepton.run/api/v1/'


@dataclass
class LlamarineLM(LlamaLM):
    """Llamarine LM."""

    @classmethod
    def from_defaults(cls) -> LlamarineLM:
        """Get default Llamarine LM instance."""
        # pylint: disable=unexpected-keyword-arg
        return cls(model=DEFAULT_MODEL, api_key=DEFAULT_API_KEY, api_base=DEFAULT_API_BASE)


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('question')
    args = arg_parser.parse_args()

    print(LlamarineLM.from_defaults().get_response(prompt=args.question))
