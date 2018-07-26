"""
Tests localbuild.py
"""

import pytest

from brewblox_tools import localbuild

TESTED = localbuild.__name__


@pytest.fixture
def getenv_mock(mocker):
    return mocker.patch(TESTED + '.getenv')


@pytest.fixture
def check_output_mock(mocker):
    return mocker.patch(TESTED + '.check_output')


@pytest.fixture
def distcopy_mock(mocker):
    return mocker.patch(TESTED + '.distcopy.main')


@pytest.fixture
def deploy_docker_mock(mocker):
    return mocker.patch(TESTED + '.deploy_docker.main')


def test_localbuild(getenv_mock, check_output_mock, distcopy_mock, deploy_docker_mock):
    getenv_mock.side_effect = [
        '_name',
        '_context',
        '_file',
    ]
    check_output_mock.side_effect = [
        b'_branch\n',
        b'_OUTPUT STUFF'
    ]
    localbuild.main()
    assert distcopy_mock.call_count == 2
    assert deploy_docker_mock.call_count == 1


def test_name_error(getenv_mock):
    getenv_mock.return_value = None
    with pytest.raises(KeyError):
        localbuild.main()