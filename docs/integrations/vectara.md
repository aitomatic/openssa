# Vectara Integration

[Vectara](https://vectara.com/) is a developer-first API platform for easily building conversational search experiences that feature best-in-class Retrieval, Summarization, and “Grounded Generation” that all but eliminates hallucinations.

With OpenSSM, you can simply use `Vectara` with just a few lines of code.

```python
from openssm import VectaraSSM
ssm = VectaraSSM()
ssm.read_directory("path/to/directory")
response = ssm.discuss(conversation_id, "what is xyz?")
```

## Integration Architecture

In the OpenSSM context, Vectara is treated as a backend, as shown below..

![LlamaIndex Integration](../diagrams/ssm-llama-index-integration.drawio.png)

`LlamaIndexSSM` is simply an SSM with a passthrough (dummy) SLM that sends user queries directory to the Vectara backend.

## Roadmap
