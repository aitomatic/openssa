<!-- markdownlint-disable MD013 MD043 -->

# OpenSSA-FinanceBench Lite benchmarking

This is a lite version of the benchmarking of `OpenSSA` performance
on the `FinanceBench` dataset. We will use 1 question from the dataset to demonstrate the use of `OpenSSA` with `DANA` architecture.

## [`FinanceBench` Dataset](https://github.com/patronus-ai/financebench/blob/main/financebench_sample_150.csv)

## Getting Started with DANA Agent

Have Python 3.12 installed.

__Install__ project, and update its dependencies from time to time:
__`make install`__.

Create `.env` file following the `.env.template` and fill in necessary credentials.

__Solve__ the problem corresponding to a problem `00807` `financebench_id`:
__`make dana-solve id=00807`__.

### Question

`Does 3M have a reasonably healthy liquidity profile based on its quick ratio for Q2 of FY2023? If the quick ratio is not relevant to measure liquidity, please state that and explain why.`

### Knowledge

To solve this question, you can add knowledge related to `liquidity`. See the example below:

- Liquidity Metric Formulas
  - `(Net) Working Capital` = `(Total) Current Assets` - `(Total) Current Liabilities`
  - `Working Capital Ratio` = `(Total) Current Assets` / `(Total) Current Liabilities`

Go to `knowledge-store.txt` to add relevant knowledge yourself and see how it helps the agent to solve this question.

### Program

With the above-provided knowledge, the program we can provide to the agent could be as below:

- Goal: To assess liquidity health of a company, calculate `quick ratio`
  - Task: To calculate `quick ratio`, use this formula
            `Quick Ratio` = (
          (`Cash & Cash Equivalents` +
           `Short-Term Investments or (Current) Marketable Securities` +
           `(Net) Accounts Receivable, a.k.a. (Net) (Trade) Receivables`)
          / `(Total) Current Liabilities`
        )
        - Sub-task 1: What are values in dollars of `Cash & Cash Equivalents`?
        - Sub-task 2: What are values in dollars of `Short-Term Investments or (Current) Marketable Securities`?
        - Sub-task 3: What are values in dollars of `(Net) Accounts Receivable, a.k.a. (Net) (Trade) Receivables`?
        - Sub-task 4: What are values in dolloars of `(Total) Current Liabilities`?

Go to `program-store.yml` to see details of the program yourself! You can experimenting with different plans to see how it helps the agent solve the problem as well.

## Advancing DANA Agent with Domain Knowledge and Program Store

- To solve the question with added domain knowledge, run `make dana-solve-w-knowledge id=00807`
- To solve the question with added domain knowledge and program store, run `make dana-solve-w-knowledge-and-prog-store id=00807`
