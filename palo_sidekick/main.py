"""A collection of CLI tools for Palo Alto devices."""

import os
import sys
import xml.etree.ElementTree as ET
from operator import itemgetter
from typing import List

import click
from rich.console import Console
from rich.table import Table

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
    resource = "/?type=op&cmd=<show><devicegroups/></show>"
    response = ctx.obj.get(resource)
    root = ET.fromstring(response.text)
    device_groups = root.findall(".//devicegroups/entry")
    if not device_groups:
        return None
    device_group_names: List[str] = [dg.attrib["name"] for dg in device_groups]
    click.echo("\n".join(sorted(device_group_names)))


@_list.command(name="firewalls")
@click.pass_context
def list_firewalls(ctx: click.Context) -> None:
    """Print a list of firewalls."""
    panorama: Panorama = ctx.obj
    resource = "/?type=op&cmd=<show><devices><all/></devices></show>"
    response = panorama.get(resource)
    root = ET.fromstring(response.text)
    firewalls = root.findall(".//devices/entry/hostname")
    if not firewalls:
        return None
    click.echo("\n".join(sorted([fw.text for fw in firewalls if fw.text])))


@cli.group(name="get")
@click.pass_context
def get(ctx: click.Context) -> None:
    """Get more details on things."""


@get.command(name="firewalls")
@click.pass_context
def get_firewall_details(ctx: click.Context) -> None:
    """
    Get details on firewalls including hostname, software version,
    model, and vsys list.
    """
    ...
    resource = "/?type=op&cmd=<show><devicegroups/></show>"
    response = ctx.obj.get(resource)
    root = ET.fromstring(response.text)
    firewalls = [
        {
            "hostname": entry.findtext("hostname"),
            "model": entry.findtext("model"),
            "sw_version": entry.findtext("sw-version"),
            "ha_state": entry.findtext("ha/state"),
            "vsys_list": "\n".join(
                [vsys.attrib["name"] for vsys in entry.findall("vsys/entry")]
            ),
        }
        for entry in root.findall(".//devicegroups/entry/devices/entry")
        if entry.findtext("hostname")
    ]

    table = Table(title="Panorama Managed Firewalls")
    columns = ["Hostname", "Model", "Software", "HA State", "Vsys"]
    for column in columns:
        table.add_row(column)

    sorted_firewalls = sorted(firewalls, key=itemgetter("hostname"))
    for firewall in sorted_firewalls:
        table.add_row(*firewall.values())

    Console().print(table)


if __name__ == "__main__":
    cli()
