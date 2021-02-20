import unittest


class FailTest(unittest.TestCase):

    def test_sum_success(self):
        """ 1 + 2 = 4？ """
        a, b = 1, 2
        assert a+b == 3

    def test_sum_fail(self):
        """ 1 + 2 = 4？ """
        a, b = 1, 2
        assert a+b == 4

    def test_sum_error(self):
        """ 1 + 2 = 4？ """
        a, b = 1, 2
        raise("hhhh")