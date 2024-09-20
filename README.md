<!-- markdownlint-disable MD013 MD043 -->

# `OpenSSA`: Small Specialist Agents for Industrial AI

`OpenSSA` is an agentic AI framework for solving complex problems in real-world industry domains,
overcoming the limitations of LLMs and RAG in high-precision settings.

At the heart of this framework is a __Domain-Aware Neurosymbolic Agent (DANA)__ architecture,
which treats domain-specific knowledge as a first-class concern
and applies captured knowledge representations in neural and symbolic program search and program execution
to achieve consistency and accuracy in problem-solving.

## Level-2 Intelligence with Domain-Specific Knowledge and Sophisticated Planning & Reasoning

`OpenSSA` implements a variant of the DANA architecture,
with problem-solving programs represented in a Hierarchical Task Plan (HTP) form
and program execution by powerful Observe-Orient-Decide-Act Reasoning (OODAR)
(see [OODA comparative study](https://arxiv.org/abs/2404.11792)).
`OpenSSA` DANA agents can also be armed with diverse Resources such as files, databases and web search.

This combination of the knowledge-first DANA architecture with HTP and OODAR implementations
goes far beyond the Level-1 pattern-matching intelligence performed by LLMs and RAG
and achieves superior consistency and accuracy in deliberative/iterative multi-step problem-solving.

## Small and Resource-Efficient Agents for Practical Real-World Deployment

Such Level-2 intelligence through domain-specific knowledge and planning and reasoning
allows `OpenSSA` DANA agents to work well in many industry applications
using significantly smaller component models, thereby greatly economizing computing resources.

## Open and Extensible Architecture

Committed to promoting and supporting open development in generative AI,
`OpenSSA` would strive to integrate with a diverse array of LLM backends, especially open-source LLMs.
For example, `OpenSSA` supports `Llama` LLMs and models derived or fine-tuned from them.
If you would like certain LLMs to be supported, please suggest through a GitHub issue, or, even better, submit your PRs.

Additionally, `OpenSSA`'s core Knowledge, Planning, Reasoning and Resource interfaces
are designed with customizability and extensibility as first-class concerns,
in order to enable developers to effectively solve problems in their specific industries and specialized domains.

## Getting Started

Install by __`pip install openssa`__ on Python __3.12 or 3.13__.

- For bleeding-edge latest capabilities: __`pip install https://github.com/aitomatic/openssa/archive/main.zip`__.

Explore the `examples/` directory and developer guides and tutorials on our [documentation site](https://aitomatic.github.io/openssa).

## [API Documentation](https://aitomatic.github.io/openssa/modules)

## Contributing

We welcome contributions from the community!

- Join the discussion on our [Community Forum](https://github.com/aitomatic/openssa/discussions)
- Submit pull requests for bug fixes, enhancements, or new features

For more information, see our [Contribution Guide](CONTRIBUTING.md).
