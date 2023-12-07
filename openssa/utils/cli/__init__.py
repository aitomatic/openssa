"""OpenSSA CLI."""


from collections.abc import Sequence

import click

from .contrib.ssa_prob_solver import openssa_contrib_ssa_prob_solver_cli


__all__: Sequence[str] = ('openssa_cli',)


@click.group(name='launch',
             cls=click.Group,
             commands={'solver': openssa_contrib_ssa_prob_solver_cli},
             invoke_without_command=False,
             no_args_is_help=True,
             subcommand_metavar='OPENSSA_SUB_COMMAND',
             chain=False,
             help='OpenSSA Contrib CLI >>>',
             epilog='^^^ OpenSSA Contrib CLI',
             short_help='OpenSSA Contrib CLI',
             options_metavar='[OPTIONS]',
             add_help_option=True,
             hidden=False,
             deprecated=False)
def openssa_launch_cli():
    """Trigger OpenSSA Contrib Utilities from CLI."""


@click.group(name='openssa',
             cls=click.Group,
             commands={'launch': openssa_launch_cli},
             invoke_without_command=False,
             no_args_is_help=True,
             subcommand_metavar='OPENSSA_SUB_COMMAND',
             chain=False,
             help='OpenSSA CLI >>>',
             epilog='^^^ OpenSSA CLI',
             short_help='OpenSSA CLI',
             options_metavar='[OPTIONS]',
             add_help_option=True,
             hidden=False,
             deprecated=False)
def openssa_cli():
    """Trigger OpenSSA Utilities from CLI."""
