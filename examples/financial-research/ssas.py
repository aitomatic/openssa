from pathlib import Path

import streamlit as st

# pylint: disable=wrong-import-order,wrong-import-position
from openssa.deprecated.ooda_rag.heuristic import TaskDecompositionHeuristic
from openssa.deprecated.ooda_rag.ooda_ssa import OodaSSA

from dataproc import get_or_create_cached_dir_path  # noqa: E402
from heuristics import (  # noqa: E402
    THREE_FIN_STATEMENTS_HEURISTICS,
)


def get_or_create_ooda_ssa(company: str,
                           guiding_heuristics: str = THREE_FIN_STATEMENTS_HEURISTICS) -> OodaSSA:
    print(f'Getting OODA-RAG SSA based on {company}...')

    ssa = OodaSSA(task_heuristics=TaskDecompositionHeuristic({}),
                  highest_priority_heuristic=guiding_heuristics,
                  enable_generative=True)

    st.write('__Gathering Relevant Resources for Analysis...__')

    ssa.activate_resources((resources_path := get_or_create_cached_dir_path(company)), re_index=True)

    for resource in (p.stem
                     for p in Path(resources_path).iterdir()
                     if p.is_file() and (not p.stem.startswith('.'))):
        st.write(f'- _{resource}_')

    return ssa
