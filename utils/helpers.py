import os
from dotenv import load_dotenv

# Load .env file automatically when app starts
load_dotenv()


def get_env(key: str, default=None):
    """
    Safely get environment variables.

    Args:
        key (str): Environment variable name
        default: Default value if key not found

    Returns:
        str | None
    """
    value = os.getenv(key, default)

    if value is None or value == "":
        return default

    return value