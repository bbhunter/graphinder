"""Test main.py."""

import argparse

import pkg_resources
import pytest

from graphinder.main import __version__, argument_builder, main, validate_arguments
from graphinder.utils.logger import get_logger


def test_version() -> None:
    """version test."""
    assert __version__ == pkg_resources.get_distribution('graphinder').version, 'Version has been changed, please update the test.'


def test_argument_builder() -> None:
    """argument_builder test."""

    args: argparse.Namespace = argument_builder([])

    assert args.domain is None
    assert not args.verbose_mode
    assert not args.no_script_mode
    assert not args.no_bruteforce_mode
    assert args.reduce_mode == 100

    args = argument_builder(['-d', 'example.com'])

    assert args.domain == 'example.com'

    args = argument_builder(['--no-bruteforce'])

    assert args.no_bruteforce_mode


def test_validate_arguments() -> None:
    """validate_arguments test."""

    logger = get_logger()
    args: argparse.Namespace = argument_builder([])

    assert not validate_arguments(logger, args)

    args = argument_builder(['-d', 'example.com'])
    assert validate_arguments(logger, args)

    args = argument_builder(['--no-script', '--no-bruteforce'])
    assert not validate_arguments(logger, args)

    args = argument_builder(['-d', 'example.com', '--no-script', '--no-bruteforce'])
    assert not validate_arguments(logger, args)


@pytest.mark.asyncio
async def test_main() -> None:
    """main test."""

    assert not await main([])


@pytest.mark.asyncio
async def test_full_run() -> None:
    """Test a complete run."""

    assert (await main(['-d', 'example.com'])) == {'example.com': set()}
