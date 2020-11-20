from typing import Any

import json


def load_json(filepath: str) -> Any:

    f = open(filepath, mode="r", encoding="utf8")
    data = json.load(f)
    f.close()

    return data
