"""OpenSSA Contrib SSA Problem Solver CLI."""


import os
from pathlib import Path

import click


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
    from openssa.contrib.streamlit_ssa_prob_solver import __path__  # pylint: disable=import-outside-toplevel
    os.chdir(Path(__path__[0]))
    os.system('streamlit run main.py --server.allowRunOnSave=true --server.runOnSave=true')
