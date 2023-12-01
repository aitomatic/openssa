"""OpenSSA Contrib."""


from collections.abc import Sequence

from .streamlit_ssa_prob_solver import SSAProbSolver as StreamlitSSAProbSolver


__all__: Sequence[str] = (
    'StreamlitSSAProbSolver',
)
