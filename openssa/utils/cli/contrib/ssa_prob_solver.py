"""OpenSSA Contrib SSA Problem Solver CLI."""


from collections.abc import Sequence
import os

import click

from openssa.contrib.streamlit_ssa_prob_solver import __path__


__all__: Sequence[str] = ('openssa_contrib_ssa_prob_solver_cli',)


@click.command(name='solver',
               cls=click.Command,
               context_settings=None,
               help=('OpenSSA Contrib SSA Problem Solver CLI >>>'),
               epilog=('^^^ OpenSSA Contrib SSA Problem Solver CLI'),
               short_help='OpenSSA Contrib SSA Problem Solver CLI',
               options_metavar='',
               add_help_option=True,
               hidden=False,
               deprecated=False)
def openssa_contrib_ssa_prob_solver_cli():
    """Launch StreamlitSSAProbSolver."""
    os.system(f'streamlit run {__path__[0]}/main.py --server.allowRunOnSave=true --server.runOnSave=true')
