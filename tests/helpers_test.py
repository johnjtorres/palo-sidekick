"""Tests for the helpers.py file."""

import os
from typing import Any, Tuple

import pytest

from palo_sidekick.helpers import Panorama


def test_env_vars_are_set(env_vars: Tuple[str, str]) -> None:
    """Testing environment variables are set."""
    assert None not in env_vars


def test_device_groups(
    monkeypatch: pytest.MonkeyPatch, panorama: Panorama, data_dir: str
) -> None:
    """Testing XML for Panorama.device_groups is parsed correctly."""
    xml_file = "show_devicegroups.xml"
    with open(os.path.join(data_dir, xml_file)) as f:
        xml = f.read()

    def mock_xml(*args: Any, **kwargs: Any) -> str:
        return xml

    monkeypatch.setattr(Panorama, "get_device_groups", mock_xml)
    expected = ["DG-1", "DG-2", "DG-3", "DG-4", "DG-5"]
    assert expected == panorama.device_groups


def test_get_connection_error(capfd: pytest.CaptureFixture, panorama: Panorama) -> None:
    """
    Testing program exits gracefully when no connection can be made to
    Panorama.
    """
    with pytest.raises(SystemExit) as sample:
        panorama.get("/")
        assert sample.value.code == 1
    expected = f"Could not establish a connection to {panorama.hostname}.\n"
    capture = capfd.readouterr()
    assert expected == capture.err
