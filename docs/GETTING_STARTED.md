# Getting Started with OpenSSA

## Who Are You?

1. An end-user of OpenSSA-based applications

2. A developer of applications or services using OpenSSA

3. An aspiring contributor to OpenSSA

4. A committer to OpenSSA

## Getting Started as an End-User
Go straight to [OpenSSA Streamlit app](https://openssa.streamlit.app/) and start building your own SSA with your domain document today!


## Getting Started as a Developer

See some example user programs in the [examples](./examples) directory. For example, to see the sample use case on semiconductor knowledge, do:

```bash
% cd examples/semiconductor
```

### Common `make` targets for OpenSSA developers

See [MAKEFILE](dev/makefile_info.md) for more details.

```bash
% make clean
% make build
% make rebuild
% make test

% make poetry-init
% make poetry-install
% make install      # local installation of OpenSSA

% make pypi-auth    # only for maintainers
% make publish      # only for maintainers
```

## Getting Started as an Aspiring Contributor

OpenSSA is a community-driven initiative, and we warmly welcome contributions. Whether it's enhancing existing models, creating new SSMs for different industrial domains, or improving our documentation, every contribution counts. See our [Contribution Guide](../CONTRIBUTING.md) for more details.

You can begin contributing to the OpenSSA project in the `contrib/` directory.

## Getting Started as a Committer

You already know what to do.

## Community

Join our vibrant community of AI enthusiasts, researchers, developers, and businesses who are democratizing industrial AI through SSMs.  Participate in the discussions, share your ideas, or ask for help on our [Community Discussions](https://github.com/aitomatic/OpenSSA/discussions).

## License

OpenSSA is released under the [Apache 2.0 License](./LICENSE.md).

## Links

- [MAKEFILE](dev/makefile_info.md)
