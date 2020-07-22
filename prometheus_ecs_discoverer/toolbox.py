from typing import List
import pprint


def chunk_list(list_to_chunk: list, chunk_size: int) -> list:
    return [
        list_to_chunk[i : i + chunk_size]
        for i in range(0, len(list_to_chunk), chunk_size)
    ]


def extract_set(root: dict, nested_key_to_extract) -> set:
    """Extracts value for given key from every dict in root."""

    extract = set()
    for root_key in root:
        extract.add(root[root_key][nested_key_to_extract])
    return extract


def print_structure(data, name: str = "generic"):
    print("=" * 70)
    print(name)
    pprint.pprint(data)
    print(" ")


def list_to_dict(lst: List[dict], key) -> dict:
    """Turns a list of dicts into a single dict.

    :param key: The value of this key in every dict in the given list will be 
        the key in the returned dict. Therefore the values must be unique or 
        entries will be overwritten.

    Example:

    ```
    input_list = [
        {
            "key1": "hallo",
            "key2": "my"
        },
        {
            "key1": "old",
            "key2": "friend"
        }
    ]

    output_dict = {
        "hallo": {
            "key1": "hallo",
            "key2": "my"
        },
        "old": {
            "key1": "old",
            "key2": "friend"
        }
    }
    ```
    """
    dct = {}
    for item in lst:
        dct[item[key]] = item
    return dct


def validate_min_len(min_len: int, collections: list) -> None:
    for collection in collections:
        if len(collection) < min_len:
            raise ValueError(f"Collection must have min {min_len}.")
