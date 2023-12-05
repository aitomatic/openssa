"""OpenSSA CLI."""


import click


@click.group(name='openssa',
             cls=click.Group,
             commands={},
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
