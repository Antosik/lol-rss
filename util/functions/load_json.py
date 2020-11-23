from typing import Any

import json


def load_json(filepath: str) -> Any:
    """Load JSON file

    Args:
        filepath (str): Path to file

    Returns:
        Any: JSON
    """

    f = open(filepath, mode="r", encoding="utf-8")
    data = json.load(f)
    f.close()

    return data
