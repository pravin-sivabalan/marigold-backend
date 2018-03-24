
from tests import BaseTestCase

import json

class MedsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.fake_user()

    def add_med(self, **kwargs):
        return self.auth_post('/meds/add', kwargs)

    def lookup_med(self, name):
        return self.auth_post('/meds/lookup', dict(name=name))

    def test_lookup_med(self):
        rv = self.lookup_med("Ibuprofen")

        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)

        self.assertEqual(data["message"], "ok")
        self.assertGreater(len(data["matches"]), 0)

    def test_add_med(self):
        rv = self.lookup_med("Ibuprofen")

        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)

        match = data["matches"][0]

        cui = match["cui"]
        name = match["name"]

        rv = self.add_med(
            cui = cui,
            name = name,
            quantity = 10,
            notifications = [
                { "day": 2, "time": "2018-01-01:05:00:00" }
            ],
            temporary = True,
            alert_user = True
        )

        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)

        self.assertEqual(data["message"], "ok")
