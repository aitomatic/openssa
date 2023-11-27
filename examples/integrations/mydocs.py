# Import OpenSSM package "live" from the source code
import sys
from pathlib import Path
sys.path.insert(0, str(Path('../../').resolve()))

import textwrap
wrapper = textwrap.TextWrapper(width=70)

from openssm import LlamaIndexSSM
ssm = LlamaIndexSSM(name="mydocs")
ssm.read_directory()

def ask(question):
    print(f"Q: {question}")
    answer = ssm.discuss(question)['content']
    answer = wrapper.wrap(answer)
    answer = '\n'.join(answer)
    print(f"A: {answer}\n")

ask("Who is Dr. S?")
ask("Who is ACP ?")
ask("What is Dr. S’s educational history?")
ask("What is ACP’s work history?")
