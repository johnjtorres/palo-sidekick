"""Tests for the helpers.py file."""

import os
from typing import Any, Optional, Tuple

import pytest

from palo_sidekick.helpers import Panorama


@pytest.fixture(scope="session")
def data_dir() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "data")


@pytest.fixture(scope="session")
def env_vars() -> Tuple[Optional[str], Optional[str]]:
    hostname = os.getenv("PANORAMA_HOSTNAME")
    api_key = os.getenv("PANORAMA_KEY")
    return hostname, api_key


def test_env_vars_exist(env_vars: Tuple[str, str]) -> None:
    assert None not in env_vars


@pytest.fixture(scope="session")
def panorama(env_vars: Tuple[str, str]) -> Panorama:
    return Panorama(*env_vars)


@pytest.fixture
def mock_get_device_groups(monkeypatch: pytest.MonkeyPatch, data_dir: str) -> None:
    xml_file = "show_devicegroups.xml"
    with open(os.path.join(data_dir, xml_file)) as f:
        xml = f.read()

    def mock_xml(*args: Any, **kwargs: Any) -> str:
        return xml

    monkeypatch.setattr(Panorama, "get_device_groups", mock_xml)


def test_device_groups(mock_get_device_groups: str, panorama: Panorama) -> None:
    expected = ["DG-1", "DG-2", "DG-3", "DG-4", "DG-5"]
    assert expected == panorama.device_groups
