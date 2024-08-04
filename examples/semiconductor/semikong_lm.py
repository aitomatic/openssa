from __future__ import annotations

from argparse import ArgumentParser
from dataclasses import dataclass

from openssa.core.util.lm.openai import OpenAILM


DEFAULT_MODEL = 'pentagoniac/SEMIKONG-70B'
DEFAULT_API_KEY = '...'
DEFAULT_API_BASE = 'http://34.44.90.64:8081/v1'


@dataclass
class SemiKongLM(OpenAILM):
    """SemiKong LM."""

    @classmethod
    def from_defaults(cls) -> None:
        """Get default SemiKong LM instance."""
        return cls(model=DEFAULT_MODEL, api_key=DEFAULT_API_KEY, api_base=DEFAULT_API_BASE)


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('question')
    args = arg_parser.parse_args()

    print(SemiKongLM.from_defaults().get_response(prompt=args.question))
