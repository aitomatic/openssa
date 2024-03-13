### Instruction to run finance bench dataset with OpenSSA OODA


1. Download finacial reports

```
    python data.py
```


2. Load documents and run Q&A on set of questions.

```
    python qa.py # standard RAG
    python ooda-qa.py # run with ooda
```

3. Auto resume if the run was incompleted or stopped in the middle.

```
    python qa.py
    python ooda-qa.py
```


4. Output

```
    tmp/finance-bench/output.csv
```
