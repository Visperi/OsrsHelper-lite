"""
MIT License

Copyright (c) 2020 Visperi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import Union, Any, Dict, Tuple, ItemsView, KeysView, ValuesView, Iterable
from collections.abc import MutableMapping
import datetime


class CacheItem:
    """
    Encapsulates the actual value and some extra internal values for items stored into Cache.
    """

    def __init__(self, value: Any):
        self.last_hit = datetime.datetime.utcnow()
        self.value = value
        self.total_hits = 0

    def _hit(self):
        """
        Update internal data of the cache item. These values measure when and how many times this item has
        been requested.
        """
        self.last_hit = datetime.datetime.utcnow()
        self.total_hits += 1


# noinspection PyProtectedMember
class Cache(MutableMapping):
    """
    Caching class for storing any types of data. Items in cache are internally stored as CacheItem objects, but their
    values are returned instead unless specific collection commands are used.
    """

    def __init__(self, name: str = None, allow_type_override: bool = True):
        """
        :param name: Optional name for the cache.
        :param allow_type_override: If True, values stored into cache can be any type. If false, trying to overwrite
                                    an existing cache item with different type of value raises an error.
        """
        self.__cache: Dict[str, CacheItem] = {}
        self.item_lifetime: Union[None, int] = None
        self.allow_type_override: bool = allow_type_override
        self.name: str = name

    def __contains__(self, item: str) -> bool:
        return item in self.__cache

    def __len__(self):
        return len(self.__cache)

    def __getitem__(self, cache_key: str) -> Any:
        cache_item = self.__cache[cache_key]
        cache_item._hit()
        return cache_item.value

    def __setitem__(self, cache_key: str, value: Any):

        new_item = CacheItem(value)
        if self.allow_type_override:
            self.__cache[cache_key] = new_item
            return

        # Overriding cache items with new types is now allowed
        try:
            existing = self[cache_key]
            if type(existing) != type(value):
                raise TypeError(f"Different type of cache item already owns key \"{cache_key}\" (expected "
                                f"type {type(existing)}, got type {type(value)}")
        except KeyError:
            self.__cache[cache_key] = new_item

    def __iter__(self) -> Iterable[Tuple[str, CacheItem]]:
        yield from self.__cache.items()

    def __delitem__(self, cache_key: str):
        del self.__cache[cache_key]

    def __repr__(self):
        return repr(self.__cache)

    def __str__(self):
        return str(self.__cache)

    def pop(self, cache_key: str) -> Any:
        """
        Pop an item from cache.

        :param cache_key: Key to search from cache
        :return: The value of popped item
        """
        return self.__cache.pop(cache_key).value

    def popitem(self) -> Tuple[str, Any]:
        """
        Pop the last added item from cache.

        :return: Tuple containing the cache key and the value stored into it
        """

        lifo_item = self.__cache.popitem()
        return lifo_item[0], lifo_item[1].value

    def items(self) -> ItemsView[str, CacheItem]:
        """
        Return the cache contents as a raw CacheItem objects in an ordinary ItemsView

        :return: ValuesView of the cache keys and respective CacheItem objects
        """
        return self.__cache.items()

    def keys(self) -> KeysView[str]:
        """
        Get the cache keys as an ordinary KeysView.
        """
        return self.__cache.keys()

    def values(self) -> ValuesView[CacheItem]:
        """
        Get the items stored in cache as an ordinary ValuesView collection of CacheItem objects.
        """
        return self.__cache.values()

    def clear(self):
        """
        Clear the cache from items. Choose wisely.
        """
        self.__cache.clear()

    def get(self, cache_key: str, default=None) -> Any:
        """
        Get a cache item. If not found, return the default value instead.

        :param cache_key: Key to be searched from cache
        :param default: Value that is returned if cache item is not found
        :return: Cache item or the default value
        """
        try:
            return self[cache_key]
        except KeyError:
            return default

    def set_item_lifetime(self, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0):
        """
        Set item lifetime for cached items. The total value is converted into total seconds. This value is then used to
        decide deleted items when deleting deprecated items.

        Available to set more complex lifetimes easily instead of calculating seconds manually.

        :param seconds:
        :param minutes:
        :param hours:
        :param days:
        """
        total_seconds = seconds

        total_seconds += minutes * 60
        total_seconds += hours * 3600
        total_seconds += days * 3600 * 24

        if total_seconds < 0:
            raise ValueError("Item lifetime can not be a negative value.")

        self.item_lifetime = total_seconds

    def reset_item_lifetime(self):
        """
        Reset the item lifetime to None, which in practice means an infinite lifetime. Available just to encapsulate
        this operation into a safe method.

        :return:
        """
        self.item_lifetime = None

    def add(self, value: Any, cache_key: str = None):
        """
        Add an item into cache. Available to offer a way to call this operation just by giving the cached item. If no
        cache key is given, str() method for the item is called and the return value used as key.

        :param value: Value to be stored into cache
        :param cache_key: Cache key for the item. If None, str(value) is used as the key
        """
        if not cache_key:
            self[str(value)] = value
        elif isinstance(cache_key, str):
            self[cache_key] = value
        else:
            raise TypeError("Cache keys must be strings.")

    def delete(self, cache_key: str) -> None:
        """
        Delete an item from cache. Available just to offer a visible counterpart method for add().
        Normal dictionary operations are supported and may usually be better to achieve the same result.

        :param cache_key: Key which the item is saved into
        """
        del self[cache_key]

    def delete_deprecated(self) -> int:
        """
        Delete cache items based on the last time they were requested from cache. All items that have bigger than item
        lifetime difference between their last hit and current time, are deleted.

        Does nothing if item lifetime is None.

        :return: Number of deleted items
        """
        if not self.item_lifetime:
            return 0

        tmp = {}
        current_dt = datetime.datetime.utcnow()
        # Make a new dict of current cache contents which last hits are recent enough
        for cache_key, cache_item in self.items():
            if (current_dt - cache_item.last_hit).total_seconds() < self.item_lifetime:
                tmp[cache_key] = cache_item

        deleted_items = len(self) - len(tmp)
        self.__cache = tmp
        return deleted_items

    def delete_unpopular(self, hits_limit: int) -> int:
        """
        Delete cache items based on their number of total hits. All items that have less than given number of total
        hits are deleted.

        :param hits_limit: Lower limit for total hits
        :return: Number of deleted cache items
        """
        if hits_limit < 0:
            raise ValueError("Hits limit must be equal or greater than zero.")

        tmp = {}
        for cache_key, cache_item in self.items():
            if cache_item.total_hits >= hits_limit:
                tmp[cache_key] = cache_item

        deleted_items = len(self) - len(tmp)
        self.__cache = tmp
        return deleted_items
