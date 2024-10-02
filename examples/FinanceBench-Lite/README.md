<!-- markdownlint-disable MD043 -->

# OpenSSA-FinanceBench Lite benchmarking

This is a lite version of the benchmarking of `OpenSSA` performance
on the `FinanceBench` dataset.

## [`FinanceBench` Dataset](https://github.com/patronus-ai/financebench/blob/main/financebench_sample_150.csv)

## Running Aitomatic SSA benchmarking project

Have Python 3.12 installed.

__Install__ project, and update its dependencies from time to time:
__`make install`__.

Create `.env` file following the `.env.template` and fill in necessary credentials.

__Solve__ the problem corresponding to a specific `financebench_id`:
__`make dana-solve id=...`__. (eg: `make dana-solve id=00807`)

- refer to `FinanceBench` dataset above for `financebench_id`s
and corresponding information
