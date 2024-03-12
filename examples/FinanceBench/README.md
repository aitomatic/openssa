<!-- markdownlint-disable MD043 -->

# OpenSSA-FinanceBench benchmarking

This example conducts the benchmarking of `OpenSSA` performance
on the `FinanceBench` dataset.

## [`FinanceBench` Dataset](https://github.com/patronus-ai/financebench/blob/main/financebench_sample_150.csv)

## Running Aitomatic SSA benchmarking project

Have Python 3.12 installed.

__Install__ project, and update its dependencies from time to time:
__`make install`__.

Create `.env` file following the `.env.template` and fill in necessary credentials.

__Solve__ the problem corresponding to a specific `financebench_id`:
__`make solve id=...`__.

- refer to `FinanceBench` dataset above for `financebench_id`s
and corresponding information
