import builtins
import sys
from typing import List

import prettyprinter

builtins.pretty = prettyprinter.pprint
builtins.cpretty = prettyprinter.cpprint


# Copyright 2020 Tim Schwenke. Licensed under the Apache License 2.0


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


def pstruct(structure, name: str = "generic structure") -> None:
    """Print given structure in a pretty way with prettyprinter"""

    sys.stdout = sys.stderr
    print(f"{name}".center(80, "-"))
    pretty(structure, indent=2)
    print(" ")
    sys.stdout = sys.__stdout__


def validate_min_len(min_len: int, collections: list) -> None:
    for collection in collections:
        if len(collection) < min_len:
            raise ValueError(f"Collection must have min {min_len}.")


def extract_env_var(container: dict, name: str) -> str or None:
    for entry in container.get("environment", []):
        if entry["name"] == name:
            return entry["value"]
    return None


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
