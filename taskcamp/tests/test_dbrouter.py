from django.test import TestCase

from taskcamp.dbrouter import SimpleDBRouter


class SimpleDBRouterTestCase(TestCase):
    def setUp(self) -> None:
        self.db_router = SimpleDBRouter()

    def test_db_master(self):
        self.assertEqual(self.db_router.db_for_write(model=None), "master")

    def test_db_replica(self):
        self.assertEqual(self.db_router.db_for_read(model=None), "replica")

    def test_db_allow_relation(self):
        self.assertTrue(self.db_router.allow_relation(obj1=None, obj2=None))

    def test_allow_migrate(self):
        self.assertTrue(
            self.db_router.allow_migrate(db="master", app_label=None, model_name=None)
        )
