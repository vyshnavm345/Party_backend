import os

import pytest
from dotenv import load_dotenv


@pytest.fixture(autouse=True)
def load_env():
    load_dotenv()
    assert os.getenv("POSTGRES_DB") is not None  # Ensures the DB variable is loaded
