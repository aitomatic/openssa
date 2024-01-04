# Lepton.AI Integration

[Lepton.AI](https://lepton.ai) is a developer-centric platform to build, fine-tune, and deploy large models.

With OpenSSA, you can create SSAs by calling the Lepton pipeline with just a few lines of code.

```python
from OpenSSA import BaseSSA, LeptonSLMFactory
ssa = BaseSSA(slm=LeptonSLMFactory.create())
response = ssa.discuss(conversation_id, "what is abc?")
```

## Integration Architecture

In the OpenSSA context, Lepton helps finetune and distill the SLM (small language model) that front-ends an ssa.

```python
![Lepton Integration](../diagrams/ssa-lepton-integration.drawio.png)
```

## Roadmap
