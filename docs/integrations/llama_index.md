# LlamaIndex Integration

[LlamaIndex](https://github.com/jerryjliu/llama_index) is a popular open-source data framework that helps you connect your large language models (LLMs) to your data so you can build powerful LLM applications. 

With OpenSSM, you can simply use `LlamaIndexSSM` with just a few lines of code.

```python
from openssm import LlamaIndexSSM
ssm = LlamaIndexSSM()
ssm.read_directory("path/to/directory")
response = ssm.discuss(conversation_id, "what is xyz?")
```

## Integration Architecture

In the OpenSSM context, LlamaIndex is treated as a backend, as shown below.

![LlamaIndex Integration](../diagrams/ssm-llama-index-integration.drawio.png)

`LlamaIndexSSM` is simply an SSM with a passthrough (dummy) SLM that sends user queries directory to the LlamaIndex backend.

## Roadmap
