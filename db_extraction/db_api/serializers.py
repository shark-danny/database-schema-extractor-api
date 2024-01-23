from rest_framework import serializers
from .models import Database, Table, Column, DatabaseEngine


class EnumFieldSerializer(serializers.Field):
    """
    Custom serializer for handling EnumField.

    Attributes:
        enum_class (Enum): The Enum class associated with the field.
    """

    def to_representation(self, obj):
        return obj.value

    def to_internal_value(self, data):
        try:
            return self.enum_class[data.upper()]
        except KeyError:
            raise serializers.ValidationError(
                f"Invalid value for {self.field_name}: {data}"
            )


class DatabaseEngineSerializer(EnumFieldSerializer):
    """
    Serializer for DatabaseEngine EnumField.
    """

    enum_class = DatabaseEngine


class ColumnSerializer(serializers.ModelSerializer):
    """
    Serializer for Column model.
    """

    class Meta:
        model = Column
        fields = ["id", "name", "table"]


class TableSerializer(serializers.ModelSerializer):
    """
    Serializer for Table model.

    Includes nested serialization for related columns.
    """

    columns = ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = Table
        fields = ["id", "name", "columns", "database"]


class DatabaseSerializer(serializers.ModelSerializer):
    """
    Serializer for Database model.

    Includes nested serialization for related tables and columns.
    """

    engine = DatabaseEngineSerializer()
    tables = serializers.SerializerMethodField()

    def get_tables(self, obj):
        tables = Table.objects.filter(database=obj)
        tables_data = []

        for table in tables:
            columns = Column.objects.filter(table=table)
            columns_data = [
                {"name": column.name, "id": column.id} for column in columns
            ]
            table_data = {"name": table.name, "id": table.id, "columns": columns_data}
            tables_data.append(table_data)

        return tables_data

    class Meta:
        model = Database
        fields = ["id", "name", "host", "user", "password", "engine", "tables"]
