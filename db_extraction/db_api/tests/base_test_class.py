from django.test import TestCase

from db_api.models import Database, DatabaseEngine


class BaseTestClass(TestCase):
    def setUp(self):
        self.database = Database.objects.create(
            name="TestDatabase",
            host="localhost",
            user="testuser",
            password="testpassword",
            engine=DatabaseEngine.POSTGRESQL,
        )
