"""
Tests bump.py
"""

from subprocess import STDOUT

import pytest
from click.testing import CliRunner

from brewblox_dev import repository

TESTED = repository.__name__


@pytest.fixture
def mocked_ext(mocker):
    mocked = [
        'check_output',
        'check_call',
        'makedirs',
        'path',
        'which',
        'utils',
    ]
    return {k: mocker.patch(TESTED + '.' + k) for k in mocked}


def test_install_hub(mocked_ext):
    mocked_ext['which'].return_value = False
    repository.prepare()
    mocked_ext['check_output'].assert_called_with('sudo apt install -y gh', shell=True)


def test_git_info(mocked_ext):
    runner = CliRunner()
    assert not runner.invoke(repository.git_info).exception


def test_delta(mocked_ext):
    runner = CliRunner()
    assert not runner.invoke(repository.delta).exception


def test_compare(mocked_ext):
    runner = CliRunner()
    assert not runner.invoke(repository.compare).exception


def test_release_edge(mocked_ext):
    runner = CliRunner()
    assert not runner.invoke(repository.release_edge).exception
    assert mocked_ext['check_call'].call_count == len(repository.REPOS)

    mocked_ext['utils'].confirm.return_value = False
    assert not runner.invoke(repository.release_edge).exception
    assert mocked_ext['check_call'].call_count == len(repository.REPOS)
