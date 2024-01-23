from db_api.models import Database, DatabaseEngine, Table, Column

from db_api.tests.base_test_class import BaseTestClass


class DatabaseModelTest(BaseTestClass):
    def test_database_creation(self):
        # Test that a database instance is created correctly
        self.assertEqual(self.database.name, "TestDatabase")
        self.assertEqual(self.database.host, "localhost")
        self.assertEqual(self.database.user, "testuser")
        self.assertTrue(self.database.password.startswith("pbkdf2_sha256$"))
        self.assertEqual(self.database.engine, DatabaseEngine.POSTGRESQL)

    def test_save_method_password_hashing(self):
        # Test that the save method properly hashes the password
        database = Database(
            name="AnotherDatabase",
            host="localhost",
            user="testuser",
            password="testpassword",
            engine=DatabaseEngine.MYSQL,
        )
        database.save()
        self.assertTrue(database.password.startswith("pbkdf2_sha256$"))


class TableModelTest(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.table = Table.objects.create(database=self.database, name="TestTable")

    def test_table_creation(self):
        # Test that a table instance is created correctly
        self.assertEqual(self.table.name, "TestTable")
        self.assertEqual(self.table.database, self.database)


class ColumnModelTest(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.table = Table.objects.create(database=self.database, name="TestTable")
        self.column = Column.objects.create(table=self.table, name="TestColumn")

    def test_column_creation(self):
        # Test that a column instance is created correctly
        self.assertEqual(self.column.name, "TestColumn")
        self.assertEqual(self.column.table, self.table)
