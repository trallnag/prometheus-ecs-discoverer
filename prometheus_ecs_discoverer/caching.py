from typing import Callable, List

from loguru import logger

from prometheus_ecs_discoverer import s, telemetry, toolbox

# Copyright 2018, 2019 Signal Media Ltd. Licensed under the Apache License 2.0
# Modifications Copyright 2020 Tim Schwenke. Licensed under the Apache License 2.0


HITS = telemetry.gauge(
    "cache_hits", "Number of cache hits just before moving window.", ("name",)
)
MISSES = telemetry.gauge(
    "cache_misses", "Number of cache misses just before moving window.", ("name",)
)
CURRENT_CACHE_ENTRIES = telemetry.gauge(
    "current_cache_entries", "Number of current cache entries.", ("name",)
)
NEXT_CACHE_ENTRIES = telemetry.gauge(
    "next_cache_entries", "Number of next cache entries.", ("name",)
)


class SlidingCache:
    """Cache consisting out of two slots with a sliding window.

    Data is a nested dictionary. Works by taking a list of keys and first 
    checking the cached dict for corresponding entries. Keys without matching 
    entries are passed on to a fetch function. Other data is thrown away.

    How to use:

    ```python
    cache = SlidingCache()

    # Fetcher is used for all keys.
    data = cache.get(["my", "keys"], fetch_func)

    # Fetcher is only used for "new_key".
    # Cache now stores a total of three keys.
    data = cache.get(["keys", "new_key"], fetch_func)

    # Window is moved.
    cache.flush()

    # Cache is used.
    data = cache.get(["my"], fetch_func)

    # Window is moved.
    cache.flush()

    # Now the cache only holds the "my" key.
    # Only stuff that has been cached after the last flush.
    ```

    Attribution:

    """

    def __init__(self, name: str = "generic"):
        """
        :param name: Should describe the content / use of the cache. Used for 
            more informative logging and metrics. Defaults to "generic".
        """

        self.current = {}
        self.next = {}
        self.total_hits = 0
        self.total_misses = 0
        self.last_hits = 0
        self.last_misses = 0
        self.name = name

        self._HITS = HITS.labels(self.name)
        self._MISSES = MISSES.labels(self.name)
        self._CURRENT_CACHE_ENTRIES = CURRENT_CACHE_ENTRIES.labels(self.name)
        self._NEXT_CACHE_ENTRIES = NEXT_CACHE_ENTRIES.labels(self.name)

    def get_multiple(
        self, keys: List[str], fetch: Callable[[List[str]], List[str]],
    ) -> dict:
        """Get entries from cache and update if missing.

        Important: Don't forget the `flush()` method. Without using it the 
        cache will never remove old data and eat up more and more memory.

        :param keys: Keys to retrieve from cache.
        :param fetch: Function that fetches missing key values.
        :return: Dictionary where the keys match given keys.
        """

        self.last_hits = 0
        self.last_misses = 0

        missing = []
        result = {}

        for key in keys:
            if key in self.current:
                result[key] = self.current[key]
                self.total_hits += 1
                self.last_hits += 1
            else:
                missing.append(key)
                self.total_misses += 1
                self.last_misses += 1

        if s.DEBUG:
            logger.bind(cache=self.name, missing_keys=missing).debug(
                "{} hits. {} misses.", self.last_hits, self.last_misses,
            )

        fetched = fetch(missing) if missing else {}
        result.update(fetched)

        self.current.update(fetched)
        self.next.update(result)

        toolbox.pstruct(result) if s.PRINT_STRUCTS else None
        return result

    def get_single(self, key: str, fetch: Callable[[str], dict],) -> dict:
        """Get entry from cache and update if missing.

        Important: Don't forget the `flush()` method. Without using it the 
        cache will never remove old data and eat up more and more memory.

        :param key: Key to retrieve from cache.
        :param fetch: Function that fetches and returns missing.
        :return: Dictionary representing key value.
        """

        self.last_hits = 0
        self.last_misses = 0

        result = {}
        if key in self.current:
            result = self.current[key]
            self.total_hits += 1
            self.last_hits = 1
            logger.bind(cache=self.name, found_key=key).debug("Hit.")
        else:
            self.total_misses += 1
            self.last_misses = 1
            logger.bind(cache=self.name, missing_key=key).debug("Miss.")
            result = fetch(key)

        if result:
            self.current[key] = result
            self.next[key] = result

        toolbox.pstruct(result) if s.PRINT_STRUCTS else None
        return result

    def flush(self):
        """Slides the window making the next slot the current one."""

        logger.bind(
            hits=self.total_hits,
            misses=self.total_misses,
            entries_current=len(self.current),
            entries_next=len(self.next),
        ).info("Flush {} cache.", self.name)

        self._HITS.set(self.total_hits)
        self._MISSES.set(self.total_misses)
        self._CURRENT_CACHE_ENTRIES.set(len(self.current))
        self._NEXT_CACHE_ENTRIES.set(len(self.next))

        self.current = self.next
        self.next = {}

        self.total_hits = 0
        self.total_misses = 0
        self.last_hits = 0
        self.last_misses = 0
