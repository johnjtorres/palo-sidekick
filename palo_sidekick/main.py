#!/usr/bin/env python3

"""Main CLI application."""

import click

from palo_sidekick.helpers import get_device_groups, get_panorama


@click.group()
@click.pass_context
def cli(ctx: click.core.Context) -> None:
    """Main CLI group."""
    ctx.ensure_object(dict)
    ctx.obj["panorama"] = get_panorama()


@cli.group()
@click.pass_context
def list() -> None:
    """Print lists of objects to the terminal."""


@list.command(name="device-groups")
@click.pass_context
def list_device_groups(ctx: click.core.Context) -> None:
    """Print a list of device groups."""
    device_groups = get_device_groups(ctx.panorama)
    click.echo("\n".join([dg.name for dg in device_groups]))


if __name__ == "__main__":
    cli()
