from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from db_api.models import DatabaseEngine, Database, Table, Column
from db_api.tests.base_test_class import BaseTestClass


class DatabaseViewSetTest(APITestCase, BaseTestClass):
    def setUp(self):
        super().setUp()
        self.url = reverse("database-list")

    def test_list_databases(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "TestDatabase")

    def test_retrieve_database(self):
        retrieve_url = reverse("database-detail", args=[self.database.id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "TestDatabase")

    def test_create_database(self):
        data = {
            "name": "NewDatabase",
            "host": "newhost",
            "user": "newuser",
            "password": "newpassword",
            "engine": "MYSQL",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Database.objects.count(), 2)
        self.assertEqual(Database.objects.last().name, "NewDatabase")

    def test_update_database(self):
        update_url = reverse("database-detail", args=[self.database.id])
        data = {"name": "UpdatedDatabase"}
        response = self.client.patch(update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Database.objects.get(id=self.database.id).name, "UpdatedDatabase"
        )

    def test_delete_database(self):
        delete_url = reverse("database-detail", args=[self.database.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Database.objects.count(), 0)


class TableViewSetTest(APITestCase, BaseTestClass):
    def setUp(self):
        super().setUp()
        self.table = Table.objects.create(database=self.database, name="TestTable")
        self.url = reverse("table-list")

    def test_list_tables(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "TestTable")

    def test_retrieve_table(self):
        retrieve_url = reverse("table-detail", args=[self.table.id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "TestTable")

    def test_create_table(self):
        data = {"database": self.database.id, "name": "NewTable"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Table.objects.count(), 2)
        self.assertEqual(Table.objects.last().name, "NewTable")

    def test_update_table(self):
        update_url = reverse("table-detail", args=[self.table.id])
        data = {"name": "UpdatedTable"}
        response = self.client.patch(update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Table.objects.get(id=self.table.id).name, "UpdatedTable")

    def test_delete_table(self):
        delete_url = reverse("table-detail", args=[self.table.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Table.objects.count(), 0)

    def test_search_by_name(self):
        response = self.client.get(f'/api/tables/search_by_name/?name=TestTable')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the expected table is present in the response
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'TestTable')

    def test_search_by_name_no_results(self):
        # Search for tables containing a name that doesn't exist
        response = self.client.get('/api/tables/search_by_name/', {'name': 'nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response is an empty list
        self.assertEqual(len(response.data), 0)


class ColumnViewSetTest(APITestCase, BaseTestClass):
    def setUp(self):
        super().setUp()
        self.table = Table.objects.create(database=self.database, name="TestTable")
        self.column = Column.objects.create(table=self.table, name="TestColumn")
        self.url = reverse("column-list")

    def test_list_columns(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "TestColumn")

    def test_retrieve_column(self):
        retrieve_url = reverse("column-detail", args=[self.column.id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "TestColumn")

    def test_create_column(self):
        data = {"table": self.table.id, "name": "NewColumn"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Column.objects.count(), 2)
        self.assertEqual(Column.objects.last().name, "NewColumn")

    def test_update_column(self):
        update_url = reverse("column-detail", args=[self.column.id])
        data = {"name": "UpdatedColumn"}
        response = self.client.patch(update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Column.objects.get(id=self.column.id).name, "UpdatedColumn")

    def test_delete_column(self):
        delete_url = reverse("column-detail", args=[self.column.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Column.objects.count(), 0)
