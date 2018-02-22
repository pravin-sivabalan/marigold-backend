
import os
os.environ["MARIGOLD_CONFIG_PATH"] = os.environ.get("MARIGOLD_TEST_CONFIG_PATH", "../testing")

import flaskapp
import db.util

import unittest as ut
import json

class BaseTestCase(ut.TestCase):
    def setUp(self):
        self.app = flaskapp.app.test_client()
        self.app.testing = True

        with flaskapp.app.app_context() as ctx:
            db.util.init()

    def post(self, route, data):
        return self.app.post(route, data=json.dumps(data), content_type='application/json')

    def make_auth_headers(self):
        return dict(
            Authorization=self.jwt
        )

    def auth_get(self, route):
        return self.app.get(route, headers=self.make_auth_headers())

    def login(self, email, password):
        rv = self.post('/user/login', dict(
            email=email,
            password=password
        ))

        self.assertEqual(rv.status_code, 200)

        data = json.loads(rv.data)
        self.assertEqual(data["message"], "ok")

        self.jwt = data["jwt"]

if __name__ == "__main__":
    ut.main()
