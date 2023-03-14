import os
from typing import Optional, Tuple

import pytest

from palo_sidekick.panorama import Panorama


@pytest.fixture(scope="session")
def data_dir() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "data")


@pytest.fixture(scope="session")
def env_vars() -> Tuple[Optional[str], Optional[str]]:
    hostname = os.getenv("PANORAMA_HOSTNAME")
    api_key = os.getenv("PANORAMA_KEY")
    return hostname, api_key


@pytest.fixture(scope="session")
def panorama() -> Panorama:
    return Panorama(hostname="TEST", api_key="TEST")
