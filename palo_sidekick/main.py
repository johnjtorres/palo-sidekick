"""A collection of CLI tools for Palo Alto devices."""

import os
import sys

import click

from palo_sidekick.panorama import Panorama


@click.group(help=__doc__)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Main CLI group."""
    ctx.ensure_object(dict)
    hostname = os.getenv("PANORAMA_HOSTNAME", "")
    key = os.getenv("PANORAMA_KEY", "")
    validate_environment_variables(hostname, key)
    ctx.obj = Panorama(hostname, key)


def validate_environment_variables(hostname: str, key: str) -> None:
    """Checks PANORAMA_HOSTNAME and PANORAMA_KEY variables are defined."""
    if not all((hostname, key)):
        click.echo(
            "PANORAMA_HOSTNAME or PANORAMA_KEY environment variables not set.", err=True
        )
        sys.exit(1)


@cli.group(name="list")
@click.pass_context
def _list(ctx: click.Context) -> None:
    """Print lists of things to the terminal."""


@_list.command(name="device-groups")
@click.pass_context
def list_device_groups(ctx: click.Context) -> None:
    """Print a list of device groups."""
    device_groups = ctx.obj.device_groups
    if device_groups:
        click.echo("\n".join(sorted(ctx.obj.device_groups)))


if __name__ == "__main__":
    cli()
