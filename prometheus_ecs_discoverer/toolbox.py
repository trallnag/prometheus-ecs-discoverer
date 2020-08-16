import builtins
import sys
from typing import List

import prettyprinter

builtins.pretty = prettyprinter.pprint
builtins.cpretty = prettyprinter.cpprint

# Copyright 2020 Tim Schwenke. Licensed under the Apache License 2.0

"""
Contains a bunch of more or less generic functions that are used throughout 
this project.
"""


def chunk_list(list_to_chunk: list, chunk_size: int) -> list:
    """Chunks given list into chunks of a given size."""

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
    """Ensures a min length for all given lists.

    Args:
        min_len: Min length all lists should be.
        collections: A collection of lists.

    Raises:
        ValueError: Will be raised if a list is shorter than `min_len`.
    """
    for collection in collections:
        if len(collection) < min_len:
            raise ValueError(f"Collection must have min {min_len}.")


def extract_env_var(container: dict, name: str) -> str or None:
    """Extracts env var from container definition.

    Args:
        container: Container definition.
        name: Name of the environment variable.

    Returns:
        Enviornment variable value or `None` if var is not found.
    """

    for entry in container.get("environment", []):
        if entry["name"] == name:
            return entry["value"]
    return None


def list_to_dict(lst: List[dict], key) -> dict:
    """Turns a list of dicts into a single dict.

    Args:
        lst: List of dicts.
        key: The key in every dict in `lst` that should be used as the key for 
            the new dict. Therefore the values must be unique or entries will 
            be overwritten.

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
