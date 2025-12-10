"""Tests for the winzy hookspecs."""

from winzy.hookspecs import winzySpec


def test_winzy_spec_register_commands():
    """Test that the register_commands hookspec is properly defined."""
    spec = winzySpec()

    # Check that register_commands method exists and has correct signature
    assert hasattr(spec, 'register_commands')

    # The method should have the correct docstring
    assert spec.register_commands.__doc__ is not None
    assert "Register additional CLI sub commands" in spec.register_commands.__doc__