"""A collection of tools for Palo Alto devices."""

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
    if "" in (hostname, key):
        click.echo("PANORAMA_HOSTNAME or PANORAMA_KEY environment variables not set.")
        sys.exit(1)
    ctx.obj = Panorama(hostname, key)


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
