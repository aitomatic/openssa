<!-- markdownlint-disable MD043 -->

# OpenSSA-FinanceBench Lite benchmarking

This is a lite version of the benchmarking of `OpenSSA` performance
on the `FinanceBench` dataset. We will use 1 question from the dataset to demonstrate the use of `OpenSSA` with `DANA` architecture. 

## [`FinanceBench` Dataset](https://github.com/patronus-ai/financebench/blob/main/financebench_sample_150.csv)

## Running Aitomatic SSA benchmarking project

Have Python 3.12 installed.

__Install__ project, and update its dependencies from time to time:
__`make install`__.

Create `.env` file following the `.env.template` and fill in necessary credentials.

__Solve__ the problem corresponding to a problem `00807` `financebench_id`:
__`make dana-solve id=00807`__.

