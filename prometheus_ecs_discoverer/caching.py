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

    Data is a nested dictionary. Main method is `cached()`. Works by taking a 
    list of keys and first checking the cached dict for corresponding entries. 
    Keys without matching entries are passed on to a fetch function. Other data 
    is thrown away.

    How to use:

    ```python
    cache = SlidingCache()
    # Fetcher is used for all keys.
    data = cache.cached(["my", "keys"], fetch_func)
    # Fetcher is only used for "new_key".
    data = cache.cached(["keys", "new_key"], fetch_func)
    ```
    
    Public attributes:

    :ivar current: Dictionary that represents the current slot. Defaults to `{}`.
    :ivar next: Dictionary that becomes the `current` cache ever time `cached` 
        is called. Defaults to `{}`.
    :ivar last_hits: Number of hits occurred during the last `cached`.
    :ivar last_misses: Number of misses occurred during the last `cached`.
    """

    def __init__(self, name: str = "generic"):
        """
        :param name: Should describe the content / use of the cache. Used for 
            more informative logging and metrics. Defaults to "generic".
        """

        self.current = {}
        self.next = {}
        self._hits = 0
        self.last_misses = 0
        self.last_hits = 0
        self._misses = 0
        self._name = name

        self._HITS = HITS.labels(self._name)
        self._MISSES = MISSES.labels(self._name)

    def cached(
        self,
        allowed_keys: List[str],
        fetch_missing_data: Callable[[List[str]], List[str]],
    ) -> Dict[str, dict]:
        """Get entries, update missing and move window.

        Takes the given keys and checks retrieves matching entries from the 
        `current` cache. Keys without found values are passed to the 
        `fetch_missing_data` function. Returned data is combined with already 
        retrieved data and made into the `next` cache, which is made into the 
        `current` cache. Result is also returned, but can also retrieved by
        accessing `current` directly.

        :param allowed_keys: List of keys that represent the latest current set
            of cache keys. Their values will be moved to the next slot and 
            returned to the caller. All other entries will be deleted. List 
            elements must be unique.
        :param fetch_missing_data: Function that fetches and returns values for 
            keys to keep but not found in the current slot.
        :return: Dictionary where the keys match given keys. Important: This 
            dict represents the `current` cache. If you need to modify the 
            data deepcopy the data beforehand.
        """

        missing = []
        result = {}

        for key in allowed_keys:
            if key in self.current:
                result[key] = self.current[key]
                self._hits += 1
            else:
                missing.append(key)
                self._misses += 1

        missing = fetch_missing_data(missing)
        result.update(missing)

        self.next = result

        self._move_window()

        return self.current

    def _move_window(self):
        """Slides the window making the next slot the current one."""

        logger.info(
            (
                f"Moving window of cache name='{self._name}' with "
                f"hits='{self._hits}', misses='{self._misses}'."
            )
        )

        self._HITS.set(self._hits)
        self._MISSES.set(self._misses)

        self.current = self.next
        self.next = {}

        self.last_hits = self._hits
        self.last_misses = self._misses

        self._hits = 0
        self._misses = 0
