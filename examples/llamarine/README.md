<!-- markdownlint-disable MD043 -->

# Maritime-Specific Agent

This app serves as a proof of concept (PoC) for a maritime-specific AI agent designed to address and solve collision avoidance problems in marine navigation.

## Usage

```shell
make streamlit-run
```

## Running with Docker

If you prefer to run the app in a Docker container, follow these steps:

### Prerequisites

- Docker installed on your machine.

### Building the Docker Image

```shell
docker build -t dana-llamarine .
```

### Running the Docker Container

1. Running the container:

```shell
docker run --name llamarine-test --rm -p 8501:8501 -e .env dana-llamarine
```

2. Access the app at [http://localhost:8501](http://localhost:8501).
