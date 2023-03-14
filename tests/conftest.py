"""Configuration and fixtures for pytest."""

import os
from typing import Optional, Tuple

import pytest

from palo_sidekick.panorama import Panorama


@pytest.fixture(scope="session")
def data_dir() -> str:
    """Return the data directory where test data is stored."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "data")


@pytest.fixture(scope="session")
def env_vars() -> Tuple[Optional[str], Optional[str]]:
    """
    Return a tuple of the environment variables needed for this
    application.
    """
    hostname = os.getenv("PANORAMA_HOSTNAME")
    api_key = os.getenv("PANORAMA_KEY")
    return hostname, api_key


@pytest.fixture(scope="session")
def panorama() -> Panorama:
    """
    Return a test Panorama with a fake hostname and key. The tests don't
    rely on an live Panorama device so this is fine.
    """
    return Panorama(hostname="TEST", api_key="TEST")
