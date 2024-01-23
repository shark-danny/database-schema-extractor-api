from django.test import TestCase
from db_api.models import DatabaseEngine, Database, Table, Column
from db_api.serializers import (
    DatabaseEngineSerializer,
    ColumnSerializer,
    TableSerializer,
    DatabaseSerializer,
)
from db_api.tests.base_test_class import BaseTestClass


class EnumFieldSerializerTest(TestCase):
    def test_to_representation(self):
        serializer = DatabaseEngineSerializer()
        representation = serializer.to_representation(DatabaseEngine.POSTGRESQL)
        self.assertEqual(representation, "postgresql")

    def test_to_internal_value_valid(self):
        serializer = DatabaseEngineSerializer()
        internal_value = serializer.to_internal_value("mysql")
        self.assertEqual(internal_value, DatabaseEngine.MYSQL)


class ColumnSerializerTest(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.table = Table.objects.create(database=self.database, name="TestTable")
        self.column = Column.objects.create(table=self.table, name="TestColumn")

    def test_column_serializer(self):
        serializer = ColumnSerializer(instance=self.column)
        data = serializer.data
        self.assertEqual(data["id"], self.column.id)
        self.assertEqual(data["table"], self.column.table.id)
        self.assertEqual(data["name"], self.column.name)


class TableSerializerTest(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.table = Table.objects.create(database=self.database, name="TestTable")
        self.column = Column.objects.create(table=self.table, name="TestColumn")

    def test_table_serializer(self):
        serializer = TableSerializer(instance=self.table)
        data = serializer.data
        self.assertEqual(data["id"], self.table.id)
        self.assertEqual(data["database"], self.table.database.id)
        self.assertEqual(data["name"], self.table.name)


class DatabaseSerializerTest(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.table = Table.objects.create(database=self.database, name="TestTable")
        self.column = Column.objects.create(table=self.table, name="TestColumn")

    def test_database_serializer(self):
        serializer = DatabaseSerializer(instance=self.database)
        data = serializer.data
        self.assertEqual(data["id"], self.database.id)
        self.assertEqual(data["name"], self.database.name)
        self.assertEqual(data["host"], self.database.host)
        self.assertEqual(data["user"], self.database.user)
        self.assertEqual(data["password"], self.database.password)
        self.assertEqual(data["engine"], "postgresql")
