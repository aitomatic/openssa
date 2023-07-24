# LlamaIndex Integration

[LlamaIndex](https://github.com/jerryjliu/llama_index) is a popular open-source data framework that helps you connect your large language models (LLMs) to your data so you can build powerful LLM applications. 

With OpenSSM, you can simply use `LlamaIndexSSM` with just a few lines of code.

```python
from openssm.core.ssm.llama_index_ssm import LlamaIndexSSM

ssm = LlamaIndexSSM()
ssm.read_directory("path/to/directory")
response = ssm.query("query string")
```

## Integration Architecture

In the OpenSSM context, LlamaIndex is treated as a backend, as shown below..

![LlamaIndex Integration](../diagrams/ssm-llama-index-integration.drawio.png)
