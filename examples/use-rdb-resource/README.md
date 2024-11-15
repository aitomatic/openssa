# Access Database resources and inference by DANA

## What is this example doing?

- Use DbResource file to get data from RDB(MySQL) Using SQL made by Vanna, and answer question by DANA.

## Setting-up

- What you need
  - commands (if you are mac user, you can install those things by Homebrew)
    - mysql
      - Also, create or use existing database for this example.
    - poetry
  - API Key
    - Use your own OpenAI API key

- Setting up Commands
  - `cd examples/use-rdb-resource`
  - `poetry install`
  - `cp .env.template .env`
    - update .env data with your environment data
  - `poetry run python make_example_table_data.py`
    - if this command doesn't work, then run `poetry env use 3.12`
      - change python version to resolve dependensies version
  - `poetry run python main.py`
    - run main file to answer question by DANA using DbResource, and see the result in the terminal.
