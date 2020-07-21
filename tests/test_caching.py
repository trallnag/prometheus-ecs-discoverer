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
    keys = ["these", "are", "keys"]
    result = cache.cached(keys, fetch_missing)
    assert len(result) == 3
    assert result == {"these": DUMMY, "are": DUMMY, "keys": DUMMY}
    assert cache.last_misses == 3
    assert cache.last_hits == 0

    # Second run. Everything is cached.
    keys = ["these", "are", "keys"]
    result = cache.cached(keys, fetch_missing)
    assert len(result) == 3
    assert result == {"these": DUMMY, "are": DUMMY, "keys": DUMMY}
    assert cache.last_misses == 0
    assert cache.last_hits == 3

    # Third run. Cache reduced.
    keys = ["these", "are"]
    result = cache.cached(keys, fetch_missing)
    assert len(result) == 2
    assert result == {"these": DUMMY, "are": DUMMY}
    assert cache.last_misses == 0
    assert cache.last_hits == 2


def test_cache_no_keys():
    cache = caching.SlidingCache()

    keys = []
    result = cache.cached(keys, fetch_missing)
    assert result == {}
    assert cache.last_misses == 0
    assert cache.last_hits == 0


def test_cache_duplicated_keys():
    cache = caching.SlidingCache()

    keys = ["duplicate", "duplicate"]
    result = cache.cached(keys, fetch_missing)
    assert len(result) == 1
    assert result == {"duplicate": DUMMY}
    assert cache.last_misses == 2
    assert cache.last_hits == 0


def test_manipulate_cache():
    cache = caching.SlidingCache()

    keys = ["these", "are"]
    result = cache.cached(keys, fetch_missing)
    assert result == {"these": DUMMY, "are": DUMMY}

    # Manipulate result.
    result.update({"something": "else"})
    assert result == {"these": DUMMY, "are": DUMMY, "something": "else"}
    assert cache.current != {"these": DUMMY, "are": DUMMY}
