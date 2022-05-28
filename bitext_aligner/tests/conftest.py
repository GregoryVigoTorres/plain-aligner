import pytest
from pathlib import Path


TEST_ROOTDIR = Path(__file__).parent.resolve()


@pytest.fixture
def src_path():
    return str(TEST_ROOTDIR.joinpath('src_file.txt'))


@pytest.fixture
def tar_path():
    return str(TEST_ROOTDIR.joinpath('tar_file.txt'))


@pytest.fixture
def long_tar_path():
    return str(TEST_ROOTDIR.joinpath('long_tar_file.txt'))
