# Getting Started with OpenSSM

## Who Are You?

1. An end-user of OpenSSM-based applications

2. A developer of applications or services using OpenSSM

3. An aspiring contributor to OpenSSM

4. A committer to OpenSSM

## Getting Started as an End-User

## Getting Started as a Developer

See some example user programs in the [examples](./examples) directory. For example, to run the `chatssm` example, do:

```bash
% cd examples/chatssm
% make clean
% make
```

### Common `make` targets for OpenSSM developers

See [MAKEFILE](dev/makefile_info.md) for more details.

```bash
% make clean
% make build
% make rebuild
% make test

% make poetry-init
% make poetry-install
% make install      # local installation of openssm

% make pypi-auth    # only for maintainers
% make publish      # only for maintainers
```

## Getting Started as an Aspiring Contributor

OpenSSM is a community-driven initiative, and we warmly welcome contributions. Whether it's enhancing existing models, creating new SSMs for different industrial domains, or improving our documentation, every contribution counts. See our [Contribution Guide](../CONTRIBUTING.md) for more details.

You can begin contributing to the OpenSSM project in the `contrib/` directory.

## Getting Started as a Committer

You already know what to do.

## Community

Join our vibrant community of AI enthusiasts, researchers, developers, and businesses who are democratizing industrial AI through SSMs.  Participate in the discussions, share your ideas, or ask for help on our [Community Discussions](https://github.com/aitomatic/openssm/discussions).

## License

OpenSSM is released under the [Apache 2.0 License](./LICENSE.md).

## Links

- [MAKEFILE](dev/makefile_info.md)
