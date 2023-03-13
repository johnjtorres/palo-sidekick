"""Tests for the helpers.py file."""

import os
from typing import Any, Tuple

import pytest
import requests
import requests_mock

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


def test_device_groups_returns_none(
    monkeypatch: pytest.MonkeyPatch, panorama: Panorama, data_dir: str
) -> None:
    """Testing XML for Panorama.device_groups is parsed correctly."""
    xml_file = "show_devicegroups_none.xml"
    with open(os.path.join(data_dir, xml_file)) as f:
        xml = f.read()

    def mock_xml(*args: Any, **kwargs: Any) -> str:
        return xml

    monkeypatch.setattr(Panorama, "get_device_groups", mock_xml)
    assert panorama.device_groups is None


def test_get(capfd: pytest.CaptureFixture, panorama: Panorama) -> None:
    """Test Panorama.get function."""
    with requests_mock.Mocker() as adapter:
        url = panorama.base_url + "/"
        adapter.get(
            url,
            [
                {"exc": requests.exceptions.ConnectionError},
                {"status_code": 404, "reason": "Not Found"},
                {"status_code": 200, "reason": "OK"},
            ],
        )

        with pytest.raises(SystemExit) as raised:
            panorama.get("/")
            assert raised.value.code == 1

        expected = f"Could not establish a connection to {panorama.hostname}.\n"
        capture = capfd.readouterr()
        assert expected == capture.err

        with pytest.raises(SystemExit) as raised:
            panorama.get("/")
            assert raised.value.code == 1

        expected = "Exited due to 404 Not Found error.\n"
        capture = capfd.readouterr()
        assert expected == capture.err

        response = panorama.get("/")
        assert 200 == response.status_code
        assert "OK" == response.reason
