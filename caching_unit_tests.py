import random
import string
import unittest
from caching import Cache


class CacheTesting(unittest.TestCase):

    @staticmethod
    def generate_string(length=30):
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
        pass

    def test_iter(self):
        pass

    def test_poppers_del(self):
        pass

    def test_clear(self):
        pass

    def test_add_delete(self):
        pass

    def test_delete_deprecated(self):
        pass

    def test_item_methods(self):
        pass




if __name__ == '__main__':
    unittest.main()
