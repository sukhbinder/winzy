from unittest import mock
import sys
import os
import tempfile
import pytest

from winzy.cli import main, show_help, add_alias, install_cmd
from winzy.plugins import get_plugins


def test_show_help(capsys):
    with mock.patch("sys.argv", ["winzy"]):
        with mock.patch("winzy.plugins.load_plugins"):
            main()
            captured = capsys.readouterr()
            assert "usage: winzy [-h]" in captured.out


def test_plugins(capsys):
    with mock.patch("sys.argv", ["winzy", "plugins"]):
        main()
        captured = capsys.readouterr()
        assert "No external plugins in env." in captured.out


def test_invalid_command():
    with mock.patch("sys.argv", ["winzy", "invalid_command"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert str(e.value) == "2"  # SystemExit should be raised with code 2 (error)


def test_show_help_function(capsys):
    show_help(None)
    captured = capsys.readouterr()
    assert "winzy update" in captured.out


def test_add_alias_invalid_format(capsys):
    class Args:
        alias_cmd = "invalidformat"

    add_alias(Args())
    captured = capsys.readouterr()
    assert "Invalid alias format. Use format: alias=command" in captured.out


def test_add_alias_empty_parts(capsys):
    class Args:
        alias_cmd = "=command"

    add_alias(Args())
    captured = capsys.readouterr()
    assert (
        "Invalid alias format. Both alias name and command are required" in captured.out
    )

    class Args2:
        alias_cmd = "alias="

    add_alias(Args2())
    captured = capsys.readouterr()
    assert (
        "Invalid alias format. Both alias name and command are required" in captured.out
    )


def test_add_alias_success(monkeypatch, tmp_path):
    # Mock home directory
    home_dir = tmp_path
    monkeypatch.setenv("HOME", str(home_dir))

    # Create the bin directory
    local_bin_dir = home_dir / ".local" / "bin"
    local_bin_dir.mkdir(parents=True)

    class Args:
        alias_cmd = "myalias=echo hello"

    add_alias(Args())

    # Check if the file was created
    batch_file_path = local_bin_dir / "myalias.bat"
    assert batch_file_path.exists()

    # Check file content
    content = batch_file_path.read_text()
    assert content == "@echo off\necho hello\n"


def test_add_alias_already_exists_input_no(monkeypatch, tmp_path, capfd):
    # Create a fake home directory and pre-existing alias file
    home_dir = tmp_path
    local_bin_dir = home_dir / ".local" / "bin"
    local_bin_dir.mkdir(parents=True)
    batch_file = local_bin_dir / "existing.bat"
    batch_file.write_text("@echo off\nexisting command\n")

    # Mock input to return "n" (no overwrite)
    monkeypatch.setattr("builtins.input", lambda _: "n")
    monkeypatch.setenv("HOME", str(home_dir))

    class Args:
        alias_cmd = "existing=test command"

    add_alias(Args())
    captured = capfd.readouterr()
    assert "Operation cancelled." in captured.out


def test_add_alias_already_exists_input_yes(monkeypatch, tmp_path):
    # Create a fake home directory and pre-existing alias file
    home_dir = tmp_path
    local_bin_dir = home_dir / ".local" / "bin"
    local_bin_dir.mkdir(parents=True)
    batch_file = local_bin_dir / "existing.bat"
    batch_file.write_text("@echo off\nexisting command\n")

    # Mock input to return "y" (yes overwrite)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    monkeypatch.setenv("HOME", str(home_dir))

    class Args:
        alias_cmd = "existing=test command"

    add_alias(Args())

    # Check that the file was overwritten
    content = batch_file.read_text()
    assert content == "@echo off\ntest command\n"


def test_install_cmd_with_mock():
    # Test install_cmd function with mocked pip installation
    with mock.patch("winzy.plugins.run_module") as mock_run_module, mock.patch(
        "winzy.plugins.sys.argv", []
    ):

        class Args:
            packages = ["test-package"]
            upgrade = False
            editable = None
            force_reinstall = False
            no_cache_dir = False

        install_cmd(Args())

        # Check that run_module was called with pip
        mock_run_module.assert_called_once_with("pip", run_name="__main__")


def test_install_cmd_with_flags():
    # Test install_cmd with various flags
    with mock.patch("winzy.plugins.run_module") as mock_run_module, mock.patch(
        "winzy.plugins.sys.argv", []
    ) as mock_argv:

        class Args:
            packages = ["test-package"]
            upgrade = True
            editable = "/path/to/package"
            force_reinstall = True
            no_cache_dir = True

        install_cmd(Args())

        # Check that sys.argv was properly set before calling run_module
        mock_run_module.assert_called_once_with("pip", run_name="__main__")


def test_get_plugins_no_plugins(capsys):
    plugins = get_plugins(None)
    captured = capsys.readouterr()
    assert "No external plugins in env." in captured.out
    assert plugins == []


def test_main_with_install_command():
    with mock.patch("sys.argv", ["winzy", "install", "test-package"]), mock.patch(
        "winzy.cli.install_plugin"
    ) as mock_install_plugin, mock.patch("winzy.plugins.load_plugins"), mock.patch(
        "winzy.plugins.run_module"
    ):  # Mock run_module to prevent actual pip execution

        main()

        # Check that install_plugin was called with correct arguments
        mock_install_plugin.assert_called_once()

        # Get the arguments passed to install_plugin
        call_args = mock_install_plugin.call_args
        args_passed = call_args[0][0]  # First positional argument
        assert args_passed == ["test-package"]


def test_main_with_add_alias_command(monkeypatch, tmp_path):
    # Create a mock home directory
    home_dir = tmp_path
    local_bin_dir = home_dir / ".local" / "bin"

    with mock.patch("sys.argv", ["winzy", "add-alias", "test=echo test"]), mock.patch(
        "winzy.plugins.load_plugins"
    ), monkeypatch.context() as m:

        m.setattr("os.path.expanduser", lambda x: str(home_dir))
        m.setattr(
            "builtins.input", lambda _: "y"
        )  # Automatically confirm overwrite if needed

        main()

        # Check if the batch file was created
        batch_file_path = local_bin_dir / "test.bat"
        assert batch_file_path.exists()

        # Check the content
        content = batch_file_path.read_text()
        assert "@echo off\necho test\n" in content
