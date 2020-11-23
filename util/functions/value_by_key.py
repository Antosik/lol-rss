from typing import Any, Dict, List


def value_by_key(obj: Dict[str, Any], path: str) -> Any:
    """Get Value of Object by Key

    Args:
        obj (Dict[str, Any]): Object
        path (str): Path to value

    Returns:
        Any: Value
    """
    keys = path.split('.')
    keys.reverse()

    def shift_keys(obj: Any, keys: List[str]):

        if len(keys) == 0:
            return obj

        key = keys.pop()
        if key in obj and obj[key]:
            return shift_keys(obj[key], keys)
        return None

    return shift_keys(obj, keys)
