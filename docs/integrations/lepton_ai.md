# Lepton.AI Integration

[Lepton.AI](https://lepton.ai) is a developer-centric platform to build, fine-tune, and deploy large models.

With OpenSSM, you can create SSMs by calling the Lepton pipeline with just a few lines of code.

```python
from openssm import BaseSSM, LeptonSLMFactory
ssm = BaseSSM(slm=LeptonSLMFactory.create())
response = ssm.discuss(conversation_id, "what is abc?")
```

## Integration Architecture

In the OpenSSM context, Lepton helps finetune and distill the SLM (small language model) that front-ends an SSM.

```python
![Lepton Integration](../diagrams/ssm-lepton-integration.drawio.png)
```

## Roadmap
