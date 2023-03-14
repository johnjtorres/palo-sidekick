import pytest
from click.testing import CliRunner

from palo_sidekick.main import cli, validate_environment_variables
from palo_sidekick.panorama import Panorama


@pytest.mark.parametrize("hostname, key", [("", ""), ("A", ""), ("", "A")])
def test_validate_environment_variables_fail(hostname: str, key: str) -> None:
    with pytest.raises(SystemExit) as raised:
        validate_environment_variables(hostname, key)
    assert raised.value.code == 1


def test_validate_environment_variables_success(capfd: pytest.CaptureFixture) -> None:
    validate_environment_variables("A", "B")
    capture = capfd.readouterr()
    assert capture.err == ""


def test_list_device_groups(monkeypatch: pytest.MonkeyPatch) -> None:
    """Tests listing device groups to the screen when a list is returned."""
    device_groups = ["DG-1", "DG-2", "DG-3", "DG-4", "DG-5"]
    monkeypatch.setattr(Panorama, "device_groups", device_groups)
    result = CliRunner().invoke(cli, ["list", "device-groups"])
    expected = "\n".join(device_groups) + "\n"
    assert result.stdout == expected
    assert result.exit_code == 0


def test_list_device_groups_none(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests listing device groups to the screen when a list is not returned.
    """
    monkeypatch.setattr(Panorama, "device_groups", None)
    result = CliRunner().invoke(cli, ["list", "device-groups"])
    assert result.stdout == ""
    assert result.exit_code == 0
