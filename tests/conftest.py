import pytest
import logging
from tests.utils import get_test_data


@pytest.fixture(autouse=True)
def context():
    """Resuable fixture to pass testdata between steps"""
    context = {}
    return context


@pytest.fixture(autouse=True)
def testdata():
    """Resuable fixture to provide test data for all scenarios"""
    test_data = get_test_data()
    return test_data
