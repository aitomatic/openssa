from __future__ import annotations

import os
from argparse import ArgumentParser
from dataclasses import dataclass

from openssa.core.util.lm.llama import LlamaLM

DEFAULT_MODEL = 'llamarine-navigation'
DEFAULT_API_KEY = os.environ.get('LEPTON_API_TOKEN')
DEFAULT_API_BASE = os.environ.get('DEFAULT_API_BASE')


@dataclass
class LlamarineLM(LlamaLM):
    """Llamarine LM."""

    @classmethod
    def from_defaults(cls) -> LlamarineLM:
        """Get default Llamarine instance."""
        # pylint: disable=unexpected-keyword-arg
        print("model: ", DEFAULT_MODEL)
        print("api_base: ", DEFAULT_API_BASE)
        return cls(model=DEFAULT_MODEL, api_key=DEFAULT_API_KEY, api_base=DEFAULT_API_BASE)


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('question')
    args = arg_parser.parse_args()

    print(LlamarineLM.from_defaults().get_response(prompt=args.question))
