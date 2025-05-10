import pytest
import logging

@pytest.fixture
def log():
    return logging.getLogger(__name__)



def pytest_addoption(parser):
    parser.addoption(
        "--myarg",
        action="store",
        default="default_value",
        help="A simple custom argument for tests"
    )


@pytest.fixture
def myarg(request):
    return request.config.getoption("--myarg")