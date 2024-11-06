# conftest.py
import os

import pytest
from dotenv import load_dotenv

# # Load environment variables from the .env file
# @pytest.fixture(autouse=True)
# def load_env():
#     load_dotenv()  # This loads the .env file automatically
#     print("POSTGRES_DB:", os.getenv("POSTGRES_DB"))
#     assert os.getenv("POSTGRES_DB") is not None  # Example check, can be adjusted


@pytest.fixture(autouse=True)
def load_env():
    load_dotenv()  # Load .env file
    print("POSTGRES_DB:", os.getenv("POSTGRES_DB"))
    print("POSTGRES_USER:", os.getenv("POSTGRES_USER"))
    print("POSTGRES_PASSWORD:", os.getenv("POSTGRES_PASSWORD"))
    print("POSTGRES_HOST:", os.getenv("POSTGRES_HOST"))
    print("POSTGRES_PORT:", os.getenv("POSTGRES_PORT"))
    assert os.getenv("POSTGRES_DB") is not None  # Ensures the DB variable is loaded
