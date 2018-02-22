
from tests import BaseTestCase

import unittest as ut
import json

class UserTestCase(BaseTestCase):
    def test_register(self):
        rv = self.post('/user/register', dict(
            first_name="Test",
            last_name="User",
            email="abc@abc.com",
            password="123"
        ))

        self.assertEqual(rv.status_code, 200)
        
        data = json.loads(rv.data)
        self.assertEqual(data["message"], "ok")

    def test_login(self):
        self.test_register()
        self.login(email="abc@abc.com", password="123")

        self.assertIsNotNone(self.jwt)

    def test_profile(self):
        self.test_register()
        self.login(email="abc@abc.com", password="123")

        rv = self.auth_get('/user')
        self.assertEqual(rv.status_code, 200)

        data = json.loads(rv.data)
        profile = data["profile"]

        self.assertEqual(profile["first_name"], "Test") 
        self.assertEqual(profile["last_name"], "User") 

        self.assertEqual(profile["email"], "abc@abc.com")
