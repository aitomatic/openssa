# KBase Example

A simple knowledge-base application using the various SSMs available in the library.

## Usage

First, should have your env variable OPENAI_API_KEY set to your own key.

To run the example, use the following command:

```bash
% make run      # run the example using the Python development server
```

or

```bash
% make run-prod # run the example using the gunicorn WSGI server
```

The point your browser to [http://localhost:8080/](http://localhost:8080/)

### Common `make` targets for developers

```bash
% make clean
% make build
% make rebuild
% make test

% make run
```

See [MAKEFILE](MAKEFILE) for more details.
