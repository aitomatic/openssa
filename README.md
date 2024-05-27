<!-- markdownlint-disable MD013 MD043 -->

# OpenSSA: Small Specialist Agents

## Enabling Efficient, Domain-Specific Planning and Reasoning for AI

OpenSSA is an open-source framework for creating efficient, domain-specific agents (SSAs) that solve complex problems by incorporating advanced _Planning_ and _Reasoning_ capabilities. Read more about our [study here](https://arxiv.org/abs/2404.11792)

SSAs tackle multi-step problems that require planning and reasoning beyond traditional language models. They apply OODA for deliberative reasoning (OODAR) and iterative, hierarchical task planning (HTP). This "System-2 Intelligence" breaks down complex tasks into manageable steps. SSAs make informed decisions based on domain-specific knowledge. With OpenSSA, create agents that process, generate, and reason about information. This makes them more effective and efficient in solving real-world challenges.

## Planning and Reasoning with HTP and OODAR

SSAs with advanced P&R can be built by configurating `Plan Creation`, `Plan Execution` and `Background Knowledge`

### Plan Creation: Auto vs. Expert-Guided/Specified

- Auto plans are created by using LLMs
- Expert-Guided/Specified are created with the guidance from domain-specific experts.

### Plan Execution: Static vs. Dynamic

- Static plan: each step of the plan is executed sequentially without deviation from the initial setup. The final answer is composed by aggregating the outcomes of these sequential steps.
- Dynamic planning: each step is initially executed as in static planning, but the outputs are continually assessed bythe LLM. If a particular outcome is deemed inadequate, the plan triggers a recursive solving mechanism via OODAR to perform an initial pass.

### Background Knowledge: Generic/None vs. Salient Domain Highlights ("Cheat Sheet")

TBD

--------------------------------------------------------------------------------

## Hierarchical Task Planning (HTP)

### Why HTP?

- HTP makes complex task more solvable by breaking it down into sub-plans.

### How is HTP designed in OpenSSA?

- HTP has 2 main components:

  - **Plan Creation**: create sub-plans by either going broader (more sub-plans) or deeper (more sub-tasks)
  - **Plan Execution:** (i) integrate multiple sub- and side-results into a combined conclusion; and (ii) roll up such conclusion to super/upper-nodes

## OODA-based Reasoning (OODAR)

The Observe-Orient-Decide-Act (OODA) loop is a well-established iterative reasoning framework emphasizing continuous adaptation and decision-making in complex environments. The OODA loop consists of four main stages:

1. **Observe**: Gather information about the environment and the problem at hand;
2. **Orient**: Analyze the collected information, update the understanding of the situation, and generate potential solutions or actions;
3. **Decide**: Evaluate the potential solutions or actions and select the most appropriate one based on the current understanding; and
4. **Act**: Execute the selected solution or action and monitor its impact on the environment.

The iterative nature of the OODA loop allows for continuous refinement and adaptation based on the feedback received from the environment. By repeatedly cycling through these four stages, an agent can progressively improve its understanding of the problem, generate more relevant solutions, and make better decisions.

TODO: add examples of task broken down into OODA steps

### Key Features

- **Small**: Create lightweight, resource-efficient AI agents through model compression techniques
- **Specialist**: Enhance agent performance with domain-specific facts, rules, heuristics, and fine-tuning for deterministic, accurate results
- **Agents**: Enable goal-oriented, multi-step problem-solving for complex tasks via systematic HTP planning and OODAR reasoning
- **Integration-Ready**: Works seamlessly with popular AI frameworks and tools for easy adoption
- **Extensible Architecture**: Easily integrate new models and domains to expand capabilities
- **Versatile Applications**: Build AI agents for industrial field service, customer support, recommendations, research, and more

### Example Use Cases

#### Boost RAG Performance with Reasoning

OpenSSA significantly boosts the accuracy of Retrieval-Augmented Generation (RAG) systems. It fine-tunes the embedding or completion model with domain-specific knowledge. It also adds the ability to reason about queries and underlying documents. This powerful combination lifts RAG performance by significant margins, overcoming the limitations of generic language models.

### Getting Started

1. Install OpenSSA: `pip install openssa` (Python 3.12)
2. Explore the `examples/` directory
3. Start building your own Small Specialist Agents

Detailed tutorials and guides are available in our [Documentation](https://aitomatic.github.io/openssa).

### Roadmap

- Llama3 being default model
- Other types of planning beyond HTP being integrated
- Custom reasoners
- Facts, rules, heuristics as proper data structures (not just a knowledge text block)
- Custom resources (web search, sensors, feeds)

### Contributing

We welcome contributions from the community!

- Join the discussion on our [Community Forum](https://github.com/aitomatic/openssa/discussions)
- Explore the `contrib/` directory for ongoing work and open issues
- Submit pull requests for bug fixes, enhancements, or new features

For more information, see our [Contribution Guide](CONTRIBUTING.md).
