# OpenSSM Framework Library

![OpenSSM Key Components](../docs/diagrams/ssm-key-components.drawio.png)

## High-Level Class Diagram

![OpenSSM High-Level Class Diagram](../docs/diagrams/ssm-class-diagram.drawio.png)

## Package Structure

- `openssm`: Root package for OpenSSM.
  - `openssm.core`: Core functionalities of the SSMs.
    - `openssm.core.ssm`: Small Specialist Model (SSM) functionality.
      - `openssm.core.ssm.openai_ssm`: OpenAI API SSM implementations.
      - `openssm.core.ssm.huggingface_ssm`: HuggingFace API SSM implementations.
    - `openssm.core.slm`: Component: Small Language Model (SLM) functionality.
      - `openssm.core.ssm.openai_slm`: OpenAI API SLM implementations.
      - `openssm.core.ssm.huggingface_slm`: HuggingFace API SLM implementations.
    - `openssm.core.adapter`: Component: Interface between the SLM and the domain-knowledge backends.
    - `openssm.core.backend`: Component: Interfaces to a variety of domain-knowledge backends.
    - `openssm.core.inferencer`: Component: Inference wrapper for models behind SSM backends.
  - `openssm.capture`: Tools and APIs for capturing and encoding domain knowledge into various backends.
  - `openssm.composer`: Tools for composing multiple SSMs together.
  - `openssm.industrial`: Industrial-AI specific tools and APIs (trust, reliability, safety, etc.)
  - `openssm.integration`: Tools for integrating SSMs into industrial applications.

- `tests`: Unit tests for the framework's components (located at the top level of the project).

- `apps`: Example applications using SSMs (located at the top level of the project).

- `docs`: OpenSSM project documentation (located at the top level of the project).

## Getting Started

You can begin contributing to the OpenSSM project or use our pre-trained SSMs for your industrial projects. See our [Getting
Started Guide](link-to-guide) for more information.

## Community

Join our vibrant community of AI enthusiasts, researchers, developers, and businesses who are democratizing industrial AI
through SSMs. Participate in the discussions, share your ideas, or ask for help on our [Community Forum](link-to-forum).

## Contribute

OpenSSM is a community-driven initiative, and we warmly welcome contributions. Whether it's enhancing existing models,
creating new SSMs for different industrial domains, or improving our documentation, every contribution counts. See our
[Contribution Guide](../docs/CONTRIBUTING.md) for more details.

## License

OpenSSM is released under the [Apache 2.0 License](../LICENSE.md).
