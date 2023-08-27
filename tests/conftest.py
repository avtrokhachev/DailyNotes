import pytest
import os


@pytest.fixture(scope="session", autouse=True)
def on_test_session_start():
    os.environ['testing'] = 'True'
    yield
    os.environ.pop('testing')
