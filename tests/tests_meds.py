
from tests import BaseTestCase

class MedsTestCase(BaseTestCase):
    def test_lol(self):
        self.fake_user()

        rv = self.auth_post('/meds/add', dict(
            name="Med-X",
            dose=42,
            expir_date='01 01 1942'
        ))

        self.assertEqual(rv.status_code, 42)
