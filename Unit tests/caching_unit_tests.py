import random
import string
import unittest
import time
from caching import Cache, CacheItem


class CacheTesting(unittest.TestCase):

    @staticmethod
    def generate_string(length=30):
        """
        Generate a random string of given length.
        :return: A random string that can contain ascii letters, digits and special characters
        """
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choices(chars, k=length))

    def test_constructor(self):
        for i in range(5):
            name = self.generate_string()
            cache = Cache(name)
            self.assertEqual(name, cache.name)
            self.assertEqual(cache.allow_type_override, True)

        for j in range(5):
            cache = Cache()
            cache.allow_type_override = False
            self.assertEqual(cache.name, None)
            self.assertEqual(cache.allow_type_override, False)

    def test_contains(self):
        cache_a = Cache(self.generate_string())
        cache_b = Cache(self.generate_string())

        key1 = self.generate_string()
        key2 = self.generate_string()
        cache_a[key1] = random.randint(0, 100)
        cache_a[key2] = random.randint(0, 100)

        key3 = self.generate_string()
        cache_b[key3] = random.randint(0, 100)

        self.assertTrue(key1 in cache_a)
        self.assertTrue(key2 in cache_a)
        self.assertFalse(key3 in cache_a)

        self.assertTrue(key3 in cache_b)
        self.assertFalse(key1 in cache_b)
        self.assertFalse("afdsgfjhgfgfa" in cache_b)

    def test_len(self):
        n = 3000
        cache = Cache(self.generate_string())
        for i in range(n):
            cache.add(self.generate_string())

        self.assertEqual(len(cache), n)

    def test_getters_setters(self):
        cache = Cache()
        cache["a"] = "Single string"
        random_list = [self.generate_string() for _ in range(5)]
        cache["b"] = random_list
        cache["b"].append(50)
        cache["c"] = ""
        cache["d"] = None
        multilevel_dict = {"first": self.generate_string(),
                           "second":
                               {
                                   "list": random_list,
                                   "dict": {"cache1": Cache(),
                                            "adsfada": self.generate_string()
                                            },
                                   "cache2": Cache()
                               }
                           }
        cache["e"] = multilevel_dict
        cache["e"]["second"]["dict"]["cache1"]["testval"] = random_list
        cache[123] = True

        func_key = self.generate_string
        cache[func_key] = "Functions and builtin objects are allowed too"

        self.assertEqual(cache["a"], "Single string")
        self.assertEqual(cache["b"], random_list)
        self.assertTrue(50 in cache["b"])
        self.assertEqual(cache["c"], "")
        self.assertEqual(cache["d"], None)
        self.assertEqual(cache["e"], multilevel_dict)
        self.assertTrue("testval" in cache["e"]["second"]["dict"]["cache1"])
        self.assertEqual(cache["e"]["second"]["dict"]["cache1"]["testval"], random_list)

        self.assertEqual(cache.get("d"), None)
        self.assertEqual(cache.get("sfdsa", -1), -1)
        self.assertEqual(cache.get("e"), cache["e"])

        self.assertEqual(cache[123], True)
        self.assertEqual(cache[func_key], "Functions and builtin objects are allowed too")

    def test_iter(self):
        cache = Cache()
        d = {}

        for key in range(50):
            val = self.generate_string()
            cache[str(key)] = val
            d[str(key)] = val

        for cache_item in cache:
            self.assertEqual(cache_item[1].value, d[cache_item[0]])

    def test_poppers_del(self):
        cache = Cache()
        list_ = [1, 2, 3, 4, 5]
        cache[1.4564] = "a"
        cache["val0"] = 65465
        cache["val1"] = "aaaaa"
        cache["val2"] = list_
        cache["val3"] = list_ + [6, 7, 8]

        self.assertEqual(cache.popitem()[1], [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(cache.popitem()[1], list_)
        self.assertEqual(cache.pop("val0"), 65465)
        self.assertEqual(cache.pop(1.4564), "a")
        self.assertTrue(len(cache) == 1)

    def test_clear(self):
        cache = Cache()

        for i in range(100):
            cache[str(i)] = i

        self.assertTrue(len(cache) == 100)
        cache.clear()
        self.assertTrue(len(cache) == 0)

    # noinspection PyTypeChecker
    def test_add_delete(self):
        cache = Cache()
        cache.allow_type_override = False

        cache.add(1234)
        cache.add([x for x in range(10)])
        cache.add([random.randint(0, 100) for _ in range(10)], "randList")

        self.assertTrue(len(cache) == 3)
        cache.delete("1234")
        self.assertTrue(len(cache) == 2)
        del cache["randList"]
        self.assertTrue(len(cache) == 1)

        cache.add(123, "123")
        cache.add(123)
        cache.add("Does not raise", 123)
        self.assertRaises(TypeError, cache.add, "Should raise", "123")
        self.assertRaises(TypeError, cache.add, [], "123")
        self.assertRaises(TypeError, cache.add, 0, 123)

    def test_delete_deprecated(self):
        cache = Cache()
        cache.set_item_lifetime(seconds=1)

        for i in range(10):
            cache.add(i)
            time.sleep(0.5)

        deleted = cache.delete_deprecated()
        self.assertTrue(len(cache) == 1)
        self.assertEqual(deleted, 9)
        cache.reset_item_lifetime()
        self.assertEqual(cache.item_lifetime, None)
        cache.delete_deprecated()
        self.assertTrue(len(cache) == 1)

    def test_delete_unpopular(self):
        cache = Cache()

        for i in range(10):
            cache.add(i)

        asdf = cache["3"]
        sfdg = cache["4"]
        srgd = cache.get("3")
        jhkh = cache.get("4")

        deleted = cache.delete_unpopular(2)
        self.assertEqual(deleted, 8)
        self.assertTrue(len(cache) == 2)

    def test_delete_delegated(self):
        cache = Cache()

        def delete_item(cache_item: CacheItem):
            return cache_item.key % 10 == 0 or cache_item.value % 25 == 0

        for i in range(1, 101):
            cache[i] = i

        num_deleted = cache.delete_delegated(delete_item)
        # Should be deleted: 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 25, 75 (10 based on keys, 2 based on values)
        self.assertEqual(num_deleted, 10 + 2)

        for key, value in cache.items():
            cond = key % 10 != 0 and value.value % 25 != 0
            self.assertTrue(cond)


if __name__ == '__main__':
    unittest.main()
