"""Tests for the helpers.py file."""

from panos.panorama import DeviceGroup

from palo_sidekick.helpers import get_device_groups, get_panorama

PANORAMA = get_panorama()


def test_get_device_groups():
    devices = get_device_groups(PANORAMA)
    assert isinstance(devices, list)
    assert all(isinstance(d, DeviceGroup) for d in devices)
