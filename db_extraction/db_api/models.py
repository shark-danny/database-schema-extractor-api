from django.db import models
from enumfields import Enum, EnumField
from django.contrib.auth.hashers import make_password


class DatabaseEngine(Enum):
    """
    Enum representing different types of database engines.

    Attributes:
        POSTGRESQL (str): PostgreSQL database engine.
        MYSQL (str): MySQL database engine.
    """

    POSTGRESQL = "postgresql"
    MYSQL = "mysql"


class Database(models.Model):
    """
    Model representing a database.

    Attributes:
        name (str): The name of the database.
        host (str): The host of the database.
        user (str): The username for accessing the database.
        password (str): The password for accessing the database (hashed for security).
        engine (DatabaseEngine): The type of database engine.
    """

    name = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    engine = EnumField(DatabaseEngine)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Overrides the save method to hash the password before saving.
        """
        self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Table(models.Model):
    """
    Model representing a table in a database.

    Attributes:
        database (Database): The database to which the table belongs.
        name (str): The name of the table.
    """

    database = models.ForeignKey(Database, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Column(models.Model):
    """
    Model representing a column in a table.

    Attributes:
        table (Table): The table to which the column belongs.
        name (str): The name of the column.
    """

    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
