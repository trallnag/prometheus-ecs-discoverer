from typing import Dict, List, Callable
import logging

from prometheus_ecs_discoverer import telemetry


logger = logging.getLogger(__name__)

HITS = telemetry.gauge(
    "cache_hits", "Number of cache hits just before moving window.", ("name",)
)
MISSES = telemetry.gauge(
    "cache_misses", "Number of cache misses just before moving window.", ("name",)
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

    def get(
        self,
        allowed_keys: List[str],
        fetch_missing_data: Callable[[List[str]], List[str]],
    ) -> Dict[str, dict]:
        """Get entries from cache and update if missing.

        Important: Don't forget the `flush()` method. Without using it the 
        cache will never remove old data and eat up more and more memory.

        :param allowed_keys: Keys to retrieve from cache. Keys of missing 
            entries are passed to `fetch_missing_data`. List elements must be 
            unique.
        :param fetch_missing_data: Function that fetches and returns values for 
            keys to keep but not found in the current cache slot.
        :return: Dictionary where the keys match given keys. If you need to 
            modify the data deepcopy the data beforehand.
        """

        self.last_hits = 0
        self.last_misses = 0

        missing = []
        result = {}

        for key in allowed_keys:
            if key in self.current:
                result[key] = self.current[key]
                self.total_hits += 1
                self.last_hits += 1
            else:
                missing.append(key)
                self.total_misses += 1
                self.last_misses += 1

        missing = fetch_missing_data(missing)
        result.update(missing)

        self.current.update(missing)
        self.next.update(result)

        logger.info(
            (
                f"Retrieved keys={len(allowed_keys)} from cache name={self.name} "
                f"with last_hits={self.last_hits}, last_misses={self.last_misses}."
            )
        )

        return result

    def flush(self):
        """Slides the window making the next slot the current one."""

        logger.info(
            (
                f"Flush cache name='{self.name}' slot with "
                f"hits='{self.total_hits}', misses='{self.total_misses}'."
            )
        )

        self._HITS.set(self.total_hits)
        self._MISSES.set(self.total_misses)

        self.current = self.next
        self.next = {}

        self.total_hits = 0
        self.total_misses = 0
        self.last_hits = 0
        self.last_misses = 0
