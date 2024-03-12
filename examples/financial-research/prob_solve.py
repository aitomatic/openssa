# pylint: disable=bare-except,no-name-in-module,wrong-import-position


from pathlib import Path
import sys

import streamlit as st

import nest_asyncio

sys.path.append(str(Path(__file__).parent.parent))


from ssas import get_or_create_ooda_ssa  # noqa: E402


nest_asyncio.apply()


def solve(objective: str, company: str) -> str:
    problem: str = objective + company
    print(f'PROBLEM: "{problem}"')

    ssa = get_or_create_ooda_ssa(company)

    st.write('__Integrating Findings for Recommendation...__')
    solution = ssa.solve(problem)
    return solution
