
from tests import BaseTestCase

import unittest as ut
import json

import db

class UpdateTestCase(BaseTestCase):
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
