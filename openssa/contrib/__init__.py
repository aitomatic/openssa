"""OpenSSA Contrib.

Contributions that may or may not go into `openssa.core` and `openssa.integrations`, including:

- Candidate implementations of integrations
- Reusable application components and/or templates (e.g., Gradio, Streamlit, etc.)
"""


from collections.abc import Sequence

from .streamlit_ssa_prob_solver import SSAProbSolver as StreamlitSSAProbSolver


__all__: Sequence[str] = (
    'StreamlitSSAProbSolver',
)
