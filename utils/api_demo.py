import unittest
from libs import ddt


@ddt.ddt
class Api(unittest.TestCase):

    @ddt.data({"case_name": "test_aaa", "v1": 1}, {"case_name": "test_2", "v1": 2})
    @ddt.unpack
    def test_case(self, case_name, v1):
        self.assertEqual(v1, 1)