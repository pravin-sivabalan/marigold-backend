
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

    def get_meds(self):
        return self.auth_get('/meds/for-user')

    def autoadd_med(self, med_name, **kwargs):
        rv = self.lookup_med(med_name)

        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)

        self.assertEqual(data["message"], "ok")
        match = data["matches"][0]
        
        rv = self.add_med(
            cui = match["cui"],
            name = match["name"],
            quantity = kwargs.get("quantity") or 10,
            notifications = kwargs.get("notifications") or [{ "day": 0, "time": "2018-01-01:05:00:00" }],
            temporary = kwargs.get("temporary") or False,
            alert_user = kwargs.get("alert_user") or False
        )

        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)

        self.assertEqual(data["message"], "ok")

        return rv

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

        rv = self.add_med(
            cui = match["cui"],
            name = match["name"],
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

    def test_temporary_on(self):
        rv = self.lookup_med("Advil")

        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)

        match = data["matches"][0]

        rv = self.add_med(
            cui = match["cui"],
            name = match["name"],
            quantity = 10,
            notifications = [
                { "day": 0, "time": "2018-01-01:16:00:00" }
            ],
            temporary = True,
            alert_user = False,
        )
       
        rv = self.get_meds()

        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)

        med = data["meds"][0]
        self.assertEqual(med["temporary"], 1)

    def test_temporary_off(self):
        rv = self.lookup_med("Advil")

        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)

        match = data["matches"][0]

        rv = self.add_med(
            cui = match["cui"],
            name = match["name"],
            quantity = 10,
            notifications = [
                { "day": 0, "time": "2018-01-01:16:00:00" }
            ],
            temporary = False,
            alert_user = False,
        )

        rv = self.get_meds()

        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)

        med = data["meds"][0]
        self.assertEqual(med["temporary"], 0)

    def test_no_conflicts(self):
        self.autoadd_med("Ibuprofen")
        rv = self.autoadd_med("Zyrtec")

        data = json.loads(rv.data)
        self.assertEqual(len(data["conflicts"]), 0)

    def test_conflicts(self):
        self.autoadd_med("Digoxin")
        rv = self.autoadd_med("Quinidine")

        data = json.loads(rv.data)
        self.assertEqual(len(data["conflicts"]), 1)

