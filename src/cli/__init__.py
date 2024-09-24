import click

from src.cli.add_user import add_user_async
from src.cli.runserver import runserver


@click.group()
def cli():
    pass


def add_cli_commands():
    cli.add_command(add_user_async)
    cli.add_command(runserver)
