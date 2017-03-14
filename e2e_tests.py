import pytest


# Setup and teardown fixture
@pytest.fixture(scope="module")
def setup_and_teardown():
    # Setup
    yield
    # Teardown
    pass


# Tests
def test_get_user_list(setup_and_teardown):
    pass
