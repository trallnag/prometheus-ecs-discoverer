from typing import List, Dict

from prometheus_ecs_discoverer import caching


# ==============================================================================
# Helpers


DUMMY = {
    "dummy_key1": "dummy_value1",
    "dummy_key2": "dummy_value2",
}


def fetch_missing(keys: List[str]) -> Dict[str, dict]:
    return {key: DUMMY for key in keys}


# ==============================================================================
# Tests


def test_cache_with_expected_keys():
    cache = caching.SlidingCache()

    # First run. Nothing is cached.
    keys = ["1", "2", "3"]
    result = cache.get(keys, fetch_missing)
    assert len(result) == 3
    assert result == {"1": DUMMY, "2": DUMMY, "3": DUMMY}
    assert cache.last_misses == 3
    assert cache.last_hits == 0
    assert cache.total_misses == 3
    assert cache.total_hits == 0

    # Second run. Everything is cached.
    keys = ["2", "3"]
    result = cache.get(keys, fetch_missing)
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

    # Third run. One old key and one new one.
    keys = ["3", "4"]
    result = cache.get(keys, fetch_missing)
    assert len(result) == 2
    assert cache.last_misses == 1
    assert cache.last_hits == 1
    assert len(cache.current) == 4
    assert len(cache.next) == 2

    # Perform flush.
    cache.flush()
    assert cache.current == {"3": DUMMY, "4": DUMMY}
    assert cache.next == {}


def test_cache_no_keys():
    cache = caching.SlidingCache()

    keys = []
    result = cache.get(keys, fetch_missing)
    assert result == {}
    assert cache.last_misses == 0
    assert cache.last_hits == 0


def test_cache_duplicated_keys():
    cache = caching.SlidingCache()

    keys = ["duplicate", "duplicate"]
    result = cache.get(keys, fetch_missing)
    assert len(result) == 1
    assert result == {"duplicate": DUMMY}
    assert cache.last_misses == 2
    assert cache.last_hits == 0


def test_manipulate_cache():
    cache = caching.SlidingCache()

    keys = ["these", "are"]
    result = cache.get(keys, fetch_missing)
    assert result == {"these": DUMMY, "are": DUMMY}

    # Manipulate result.
    result.update({"these": "TEST"})
    assert cache.current == {"these": DUMMY, "are": DUMMY}
