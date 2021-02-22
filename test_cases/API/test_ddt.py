import ddt
import unittest


@ddt.ddt(testNameFormat=ddt.TestNameFormat.INDEX_ONLY)
class DoubanTest(unittest.TestCase):

    @ddt.data((1, 2), (2, 3), (3, 1), (1, 4))
    @ddt.unpack
    def test_add(self, a, b):
        print(a, b)
