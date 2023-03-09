"""Helper functions are defined here to be used in multiple commands."""

import os
from typing import List, Optional

from panos.panorama import DeviceGroup, Panorama


def get_panorama(
    hostname: Optional[str] = None, api_key: Optional[str] = None
) -> Panorama:
    """Create a Panorama object from environment variables or arguments."""
    hostname = hostname if hostname else os.getenv("PANORAMA_HOSTNAME")
    api_key = api_key if api_key else os.getenv("PANORAMA_KEY")
    assert None not in (hostname, api_key)
    return Panorama(hostname=hostname, api_key=api_key)


def get_device_groups(panorama: Panorama) -> List[DeviceGroup]:
    """Get the list of DeviceGroup objects from a Panorama."""
    panorama.refresh_devices(add=True)
    return panorama.findall(class_type=DeviceGroup)
