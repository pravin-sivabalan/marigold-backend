
import os
os.environ["MARIGOLD_CONFIG_PATH"] = os.environ.get("MARIGOLD_TEST_CONFIG_PATH", "../testing")

import flaskapp
import db.util

import unittest as ut

import json
import random
import string

def rand_str(size):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

class BaseTestCase(ut.TestCase):
    def setUp(self):
        self.app = flaskapp.app.test_client()
        self.app.testing = True

        with flaskapp.app.app_context() as ctx:
            db.util.init()

    def post(self, route, data, headers=None):
        if headers is not None:
            return self.app.post(route, data=json.dumps(data), 
                                 content_type='application/json', headers=headers)
        else:
            return self.app.post(route, data=json.dumps(data), content_type='application/json')


    def make_auth_headers(self):
        return dict(
            Authorization=self.jwt
        )

    def auth_get(self, route):
        return self.app.get(route, headers=self.make_auth_headers())

    def auth_post(self, route, data=None):
        return self.post(route, data=data, headers=self.make_auth_headers())

    def login(self, email, password, validate=True):
        rv = self.post('/user/login', dict(
            email=email,
            password=password
        ))

        if validate:
            self.assertEqual(rv.status_code, 200)

        data = json.loads(rv.data)

        if validate:
            self.assertEqual(data["message"], "ok")

        if "jwt" in data:
            self.jwt = data["jwt"]

        return rv

    def fake_user(self):
        rv = self.post('/user/register', dict(
            first_name=rand_str(10),
            last_name=rand_str(10),
            email = "{}@{}.com".format(rand_str(5), rand_str(5)),
            password = "{}@{}.com".format(rand_str(5), rand_str(5))
        ))

        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)

        self.jwt = data["jwt"]
        return rv

if __name__ == "__main__":
    ut.main()
