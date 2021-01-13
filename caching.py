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

    def __init__(self, value: Any):
        self.last_hit = datetime.datetime.utcnow()
        self.value = value
        self.total_hits = 0

    def _hit(self):
        self.last_hit = datetime.datetime.utcnow()
        self.total_hits += 1


# noinspection PyProtectedMember
class Cache(MutableMapping):

    def __init__(self, name: str = None, allow_type_override: bool = True):
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
        return self.__cache.pop(cache_key).value

    def popitem(self) -> Tuple[str, Any]:
        lifo_item = self.__cache.popitem()
        return lifo_item[0], lifo_item[1].value

    def items(self) -> ItemsView[str, CacheItem]:
        return self.__cache.items()

    def keys(self) -> KeysView[str]:
        return self.__cache.keys()

    def values(self) -> ValuesView[CacheItem]:
        return self.__cache.values()

    def clear(self):
        self.__cache.clear()

    def get(self, cache_key: str, default=None) -> Any:
        try:
            return self[cache_key]
        except KeyError:
            return default

    def set_item_lifetime(self, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0):
        total_seconds = seconds

        total_seconds += minutes * 60
        total_seconds += hours * 3600
        total_seconds += days * 3600 * 24

        if total_seconds < 0:
            raise ValueError("Item lifetime can not be a negative value.")

        if total_seconds == 0:
            self.reset_item_lifetime()
        else:
            self.item_lifetime = total_seconds

    def reset_item_lifetime(self):
        self.item_lifetime = None

    def add(self, value: Any, cache_key: str = None):
        if not cache_key:
            self[str(value)] = value
        elif isinstance(cache_key, str):
            self[cache_key] = value
        else:
            raise TypeError("Cache keys must be strings.")

    def delete(self, cache_key: str):
        del self[cache_key]

    def delete_deprecated(self) -> int:
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

    def delete_unpopular(self, hits_limit: int):
        if hits_limit < 0:
            raise ValueError("Hits limit must be equal or greater than zero.")

        tmp = {}
        for cache_key, cache_item in self.items():
            if cache_item.total_hits >= hits_limit:
                tmp[cache_key] = cache_item

        deleted_items = len(self) - len(tmp)
        self.__cache = tmp
        return deleted_items
