from typing import List

from prometheus_ecs_discoverer import caching


# ==============================================================================
# Helpers


DUMMY = {
    "dummy_key1": "dummy_value1",
    "dummy_key2": "dummy_value2",
}


def fetch_missing_multiple(keys: List[str]) -> dict:
    return {key: DUMMY for key in keys}


def fetch_missing_single(key: str) -> dict:
    return DUMMY


# ==============================================================================
# Tests


def test_cache_with_expected_keys():
    cache = caching.SlidingCache()

    # Nothing is cached.
    keys = ["1", "2", "3"]
    result = cache.get_multiple(keys, fetch_missing_multiple)
    assert len(result) == 3
    assert result == {"1": DUMMY, "2": DUMMY, "3": DUMMY}
    assert cache.last_misses == 3
    assert cache.last_hits == 0
    assert cache.total_misses == 3
    assert cache.total_hits == 0

    # Everything is cached.
    keys = ["2", "3"]
    result = cache.get_multiple(keys, fetch_missing_multiple)
    assert len(result) == 2
    assert result == {"2": DUMMY, "3": DUMMY}
    assert cache.last_misses == 0
    assert cache.last_hits == 2
    assert cache.total_misses == 3
    assert cache.total_hits == 2
    assert len(cache.current) == 3
    assert len(cache.next) == 3

    # Perform flush.
    cache.flush()
    assert cache.last_misses == 0
    assert cache.last_hits == 0
    assert cache.total_misses == 0
    assert cache.total_hits == 0
    assert cache.current == {"1": DUMMY, "2": DUMMY, "3": DUMMY}
    assert cache.next == {}

    # One old key and one new one.
    keys = ["3", "4"]
    result = cache.get_multiple(keys, fetch_missing_multiple)
    assert len(result) == 2
    assert cache.last_misses == 1
    assert cache.last_hits == 1
    assert len(cache.current) == 4
    assert len(cache.next) == 2

    # Get single.
    key = "10"
    result = cache.get_single(key, fetch_missing_single)
    assert result == DUMMY
    assert cache.last_misses == 1
    assert cache.last_hits == 0
    assert len(cache.current) == 5
    assert len(cache.next) == 3

    # Perform flush.
    cache.flush()
    assert cache.current == {"3": DUMMY, "4": DUMMY, "10": DUMMY}
    assert cache.next == {}


def test_cache_no_keys():
    cache = caching.SlidingCache()

    keys = []
    result = cache.get_multiple(keys, fetch_missing_multiple)
    assert result == {}
    assert cache.last_misses == 0
    assert cache.last_hits == 0


def test_cache_duplicated_keys():
    cache = caching.SlidingCache()

    keys = ["duplicate", "duplicate"]
    result = cache.get_multiple(keys, fetch_missing_multiple)
    assert len(result) == 1
    assert result == {"duplicate": DUMMY}
    assert cache.last_misses == 2
    assert cache.last_hits == 0


def test_manipulate_cache():
    cache = caching.SlidingCache()

    keys = ["these", "are"]
    result = cache.get_multiple(keys, fetch_missing_multiple)
    assert result == {"these": DUMMY, "are": DUMMY}

    # Manipulate result.
    result.update({"these": "TEST"})
    assert cache.current == {"these": DUMMY, "are": DUMMY}


def test_single_key_cached():
    cache = caching.SlidingCache()

    key = "1"
    result = cache.get_single(key, fetch_missing_single)
    assert result == DUMMY
    assert cache.last_hits == 0
    assert cache.last_misses == 1

    cache.flush()

    key = "1"
    result = cache.get_single(key, fetch_missing_single)
    assert result == DUMMY
    assert cache.last_hits == 1
    assert cache.last_misses == 0
    assert cache.total_hits == 1
    assert cache.total_hits == 1
