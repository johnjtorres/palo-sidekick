"""Tests for palo_sidekick.panorama."""

from typing import Tuple

import pytest
import requests
import requests_mock

from palo_sidekick.panorama import Panorama


def test_env_vars_are_set(env_vars: Tuple[str, str]) -> None:
    """Testing environment variables are set."""
    assert None not in env_vars


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
