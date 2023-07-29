# Makefile guide

We use Makefiles extensively to help make the developer’s life simpler and more efficient.
Here are the key targets for the top-level `Makefile`.

- `dev-setup`: run this first to set up your dev environment.

- `test`: perform testing on both Python and JS code found.

- `test-console`: same as `test`, but also show all output on the console.

- `lint`: run `pylint` and `eslint` on the code base.

- `pre-commit`: perform both linting and testing prior to commits, or at least pull requests.

- `build`: build the library (using poetry).

- `install`: build and perform a `pip install` from the local `.whl` outputs.

- `clean`: remove all the start from a clean slate.

- `publish`: publish the `.whl` to Pypi (for `pip install` support).

- `pypi-auth`: convenient target to set up your Pypi auth token prior to publishing

- `docs-build`:  build web-based documentation

- `docs-deploy`: deploy web-based documentation to GitHub, e.g., [aitomatic.github.io/openssm](https://aitomatic.github.io/openssm)

- Miscellaneous: internal use or sub-targets

## Links

- [GETTING STARTED](../GETTING_STARTED.md)
