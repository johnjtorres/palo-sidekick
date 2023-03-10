"""Tests for the helpers.py file."""

from click.testing import CliRunner
from panos.panorama import DeviceGroup

from palo_sidekick.helpers import get_device_groups, get_panorama
from palo_sidekick.main import cli

PANORAMA = get_panorama()


def test_get_device_groups():
    devices = get_device_groups(PANORAMA)
    assert isinstance(devices, list)
    assert all(isinstance(d, DeviceGroup) for d in devices)


def test_list_device_groups():
    runner = CliRunner()
    result = runner.invoke(cli, ["list", "device-groups"])
    assert result.exit_code == 0
