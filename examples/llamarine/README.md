<!-- markdownlint-disable MD043 -->

# Maritime-Specific Agent

This app serves as a proof of concept (PoC) for a maritime-specific AI agent
leveraging [Domain-Aware Neurosymbolic Agent (DANA)](https://arxiv.org/abs/2410.02823) architecture to address and solve
collision avoidance problems in marine navigation.

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

#### Running the container

```shell
docker run --rm -p 8501:8501 --env-file .env -v $(pwd)/output:/app/output --name llamarine-test dana-llamarine
```

#### Access the app

[http://localhost:8501](http://localhost:8501)
