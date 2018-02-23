
from tests import BaseTestCase

import unittest as ut
import json

import db

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

    def test_password_hash(self):
        self.test_register()

        conn = db.make_conn()
        cursor = conn.cursor(db.DictCursor)

        count = cursor.execute("""
            SELECT password FROM users
            WHERE id = %s
        """, [1])
        self.assertGreater(count, 0)

        user = cursor.fetchall()[0]
        self.assertNotEqual(user["password"], "123")

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

    def test_user_delete(self):
        self.test_register()
        self.login(email="abc@abc.com", password="123")
        
        rv = self.auth_post('/user/delete')
        self.assertEquals(rv.status_code, 200)

        rv = self.login(email="abc@abc.com", password="123", validate=False)
        self.assertEqual(rv.status_code, 400)

        data = json.loads(rv.data)
        self.assertEqual(data["name"], "UserNotFound")
