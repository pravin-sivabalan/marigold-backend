
import unittest as ut
from tests import BaseTestCase

class UserTestCase(BaseTestCase):
    def test_f(self):
        self.assertEqual(1, 1)

if __name__ == "__main__":
    ut.main()
