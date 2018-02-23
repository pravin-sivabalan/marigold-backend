
from tests import BaseTestCase

import json

class MedsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.fake_user()

    def add_med(self, name, dose, expir_date):
        return self.auth_post('/meds/add', dict(
            name=name,
            dose=dose,
            expir_date=expir_date
        ))

    def test_add_med(self):
        rv = self.add_med(
            name="Med-X",
            dose=42,
            expir_date='01 01 1942'
        )

        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)

        self.assertEqual(data["message"], "ok")

    def test_list_meds(self):
        med1 = dict(
            name="X",
            dose=1,
            expir_date='01 01 2001'
        )

        med2 = dict(
            name="Y",
            dose=2,
            expir_date='01 29 2002'
        )

        med3 = dict(
            name="Z",
            dose=42,
            expir_date='12 04 2002'
        )

        meds_to_ins = [med1, med2, med3]
        for med in meds_to_ins:
            rv = self.add_med(**med)
            self.assertEqual(rv.status_code, 200)

        rv = self.auth_get('/meds/for-user')
        self.assertEqual(rv.status_code, 200)
        
        data = json.loads(rv.data)
        self.assertEqual(data["message"], "ok")

        meds = data["meds"]
        self.assertEqual(len(meds), 3)

    def test_med_delete(self):
        self.fake_user()

        rv = self.add_med(
            name="DELETE",
            dose=42,
            expir_date='01 01 1998'
        )
        self.assertEqual(rv.status_code, 200)
    
        rv = self.auth_post('/meds/delete', dict(
            id=1
        ))
        self.assertEqual(rv.status_code, 200)

        data = json.loads(rv.data)
        self.assertEqual(data["message"], "ok")

        rv = self.auth_get('/meds/for-user')
        data = json.loads(rv.data)
        self.assertEqual(data["message"], "ok")

        meds = data["meds"]
        self.assertEqual(len(meds), 0) 
