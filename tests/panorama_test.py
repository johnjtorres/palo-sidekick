"""Tests for palo_sidekick.panorama."""

import os
from typing import Tuple

import pytest
import requests
import requests_mock

from palo_sidekick.panorama import Panorama


def test_env_vars_are_set(env_vars: Tuple[str, str]) -> None:
    """Testing environment variables are set."""
    assert None not in env_vars


def test_device_groups_success(
    requests_mock: requests_mock.Mocker, panorama: Panorama, data_dir: str
) -> None:
    """
    Testing XML for Panorama.device_groups is parsed correctly if device
    groups exist.
    """
    xml_file = "show_devicegroups.xml"
    with open(os.path.join(data_dir, xml_file)) as f:
        xml = f.read()

    resource = "/?type=op&cmd=<show><devicegroups/></show>"
    url = panorama.base_url + resource
    requests_mock.get(url, text=xml)
    expected = ["DG-1", "DG-2", "DG-3", "DG-4", "DG-5"]
    assert expected == panorama.device_groups


def test_device_groups_returns_none(
    requests_mock: requests_mock.Mocker, panorama: Panorama, data_dir: str
) -> None:
    """
    Testing XML for Panorama.device_groups is parsed correctly if no
    device groups are found.
    """
    xml_file = "show_devicegroups_none.xml"
    with open(os.path.join(data_dir, xml_file)) as f:
        xml = f.read()

    resource = "/?type=op&cmd=<show><devicegroups/></show>"
    url = panorama.base_url + resource
    requests_mock.get(url, text=xml)
    assert panorama.device_groups is None


def test_panorama_get_connection_error_handled(
    capfd: pytest.CaptureFixture, panorama: Panorama
) -> None:
    """Test for Panorama.get raising ConnectionError."""
    with requests_mock.Mocker() as adapter:
        url = panorama.base_url + "/"
        adapter.get(url, exc=requests.exceptions.ConnectionError)

        with pytest.raises(SystemExit) as raised:
            panorama.get("/")
        assert raised.value.code == 1

        expected = f"Could not establish a connection to {panorama.hostname}.\n"
        capture = capfd.readouterr()
        assert expected == capture.err


def test_panorama_get_http_error_handled(
    capfd: pytest.CaptureFixture, panorama: Panorama
) -> None:
    """Test for Panorama.get raising HTTPError"""
    with requests_mock.Mocker() as adapter:
        url = panorama.base_url + "/"
        adapter.get(url, status_code=404, reason="Not Found")

        with pytest.raises(SystemExit) as raised:
            panorama.get("/")
            assert raised.value.code == 1

        expected = "Exited due to 404 Not Found error.\n"
        capture = capfd.readouterr()
        assert expected == capture.err


def test_panorama_get_success(panorama: Panorama) -> None:
    """Test for Panorama.get successful response."""
    with requests_mock.Mocker() as adapter:
        url = panorama.base_url + "/"
        adapter.get(url, status_code=200, reason="OK")

        response = panorama.get("/")
        assert 200 == response.status_code
        assert "OK" == response.reason
