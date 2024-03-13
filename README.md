<!-- markdownlint-disable MD013 -->

# `OpenSSA`: Unmatched Accuracy, Powered by Domain Knowledge

Struggling with accuracy on your RAG projects? You're not alone.

The core problem? Generic language models, which fall short in delivering the accuracy and relevance required for complex, multi-step problems.

Meet OpenSSA — an open-source framework that boosts RAG accuracy to a minimum of 80% by leveraging domain-specific fine-tuned models.

> __Documentation__: [aitomatic.github.io/openssa](https://aitomatic.github.io/openssa)
>
> __Installation__: `pip install openssa` _(Python 3.12)_

## Features

## Context 
### The Challenge
Retrieval-Augmented Generation (RAG) has transformed the way we approach question-answering with AI. Yet, even the most advanced RAG applications hit a common set of challenges:

Limited Accuracy: Despite their vast knowledge base, generic language models often lack the depth needed for high-accuracy outcomes in specialized domains. This limitation leads to a significant accuracy gap, making it tough for developers to meet the demands of complex AI projects.

Lack of Advanced Problem-Solving: Beyond accuracy, the ability to plan and reason through multi-step problems is critical. Generic foundation models, without domain-specific tuning, struggle to navigate the complexity of such tasks, limiting the potential of RAG applications in real-world problem-solving scenarios.

These challenges underscore a pivotal need: a system that not only improves accuracy by leveraging domain knowledge but also enhances the ability to tackle complex problems with sophisticated planning and reasoning.

### The Solution
OpenSSA is designed to overcome the limitations when using generic language models. By integrating domain-specific fine-tuned models, OpenSSA enhances the accuracy and depth of understanding for specialized tasks, pushing the boundaries of what's achievable with AI in specific domains.

Further advancements in OpenSSA aim to incorporate planning and reasoning capabilities, enabling AI to navigate through multi-step problem-solving processes more effectively. This evolution will mark a significant leap towards autonomous agentic systems capable of addressing complex challenges with nuanced, context-aware solutions.

## Getting Involved
We welcome contributions from the community! Whether you're interested in adding new models, improving the framework, or providing feedback, your input is valuable. Check out our [Community Discussions](https://github.com/aitomatic/openssa/discussions).

### As a Developer
See some example user programs in the [examples/](./examples/) directory.

### As an Aspiring Contributor
OpenSSA is a community-driven initiative, and we welcome contributions. Whether it's enhancing existing models, creating new SSAs for different domains, or improving our documentation, every contribution counts. See our [Contribution Guide](../CONTRIBUTING.md) for more details.

You can begin contributing to the OpenSSA project in the `contrib/` directory.

### As a Committer
You already know what to do :)

## Community
Join our vibrant community of AI enthusiasts, researchers, developers.  Participate in the discussions, share your ideas, or ask for help on our [Community Discussions](https://github.com/aitomatic/openssa/discussions).

## License
OpenSSA is released under the [Apache 2.0 License](LICENSE.md).

## [API References](modules)

## Note: Lepton API Key

Head to [Lepton](https://dashboard.lepton.ai/) to get your API key.

- Go to `Settings`
- Select `API tokens`
- Copy `<YOUR_LEPTON_API_TOKEN>`

In terminal, run

```bash
export LEPTON_API_KEY=<YOUR_LEPTON_API_TOKEN>
```
