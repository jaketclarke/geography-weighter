"""
Fixture set for tests
"""
import pytest
from guts.functions import empty_directory

@pytest.fixture()
def ensure_clean_output():
    """
    Deletes files from default output directory to ensure tests function properly
    """
    empty_directory('output')
    return True
