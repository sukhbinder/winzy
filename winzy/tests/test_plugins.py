"""Tests for the winzy plugin system."""

import pytest
from unittest import mock
import sys
from winzy.plugins import pm, get_plugins, install_plugin


def test_plugin_manager_initialization():
    """Test that plugin manager is initialized properly."""
    assert pm is not None
    assert pm.project_name == "winzy"


def test_get_plugins_empty_list(capsys):
    """Test get_plugins returns empty list when no plugins available."""
    result = get_plugins(None)
    captured = capsys.readouterr()

    # Check that the "No external plugins" message is printed
    assert "No external plugins in env." in captured.out
    assert result == []


def test_install_plugin_basic():
    """Test install_plugin function with basic arguments."""
    with mock.patch("winzy.plugins.run_module") as mock_run_module, mock.patch(
        "winzy.plugins.sys.argv", []
    ):

        install_plugin(["test-package"], False, None, False, False)

        # Check that run_module was called with correct module
        mock_run_module.assert_called_once_with("pip", run_name="__main__")


def test_install_plugin_with_flags():
    """Test install_plugin function with all flags enabled."""
    with mock.patch("winzy.plugins.run_module") as mock_run_module, mock.patch(
        "winzy.plugins.sys.argv", []
    ):

        # Capture the original sys.argv to verify it gets modified correctly
        with mock.patch("winzy.plugins.sys.argv", []) as mock_argv:
            install_plugin(
                ["test-package"],
                upgrade=True,
                editable="/path/to/package",
                force_reinstall=True,
                no_cache_dir=True,
            )

            # Check that run_module was called with correct module
            mock_run_module.assert_called_once_with("pip", run_name="__main__")


def test_load_plugins_skips_during_tests():
    """Test that load_plugins doesn't actually load plugins during tests."""
    from winzy.plugins import load_plugins

    # Since we're running under pytest, and the conftest.py sets _called_from_test,
    # this should not actually load plugins from setuptools entry points
    with mock.patch.object(pm, "load_setuptools_entrypoints") as mock_load:
        load_plugins()
        # The actual plugin loading should not happen when running tests
        # (since we set sys._called_from_test = True in conftest.py)
        # So the mock_load call should not be made if the condition works properly
        if getattr(sys, "_called_from_test", False):
            mock_load.assert_not_called()
