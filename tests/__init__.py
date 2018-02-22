
import unittest as ut

import flaskapp
import db.util

class BaseTestCase(ut.TestCase):
    def setUp(self):
        self.app = flaskapp.app.test_client()
        self.app.testing = True

        with flaskapp.app.app_context() as ctx:
            db.util.init()

if __name__ == "__main__":
    ut.main()
