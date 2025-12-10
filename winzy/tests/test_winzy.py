from unittest import mock
import sys
import pytest

from winzy.cli import main


def test_show_help(capsys):
    with mock.patch("sys.argv", ["winzy"]):
        with mock.patch("winzy.plugins.load_plugins", []):
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
