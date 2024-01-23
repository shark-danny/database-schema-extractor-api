from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Database, Table, Column
from .serializers import DatabaseSerializer, TableSerializer, ColumnSerializer


class DatabaseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Database instances.

    Endpoints:
        - List Databases: GET /api/databases/
        - Retrieve Database: GET /api/databases/{id}/
        - Create Database: POST /api/databases/
        - Update Database: PUT /api/databases/{id}/
        - Delete Database: DELETE /api/databases/{id}/
    """

    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer


class TableViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Table instances.

    Endpoints:
        - List Tables: GET /api/tables/
        - Retrieve Table: GET /api/tables/{id}/
        - Create Table: POST /api/tables/
        - Update Table: PUT /api/tables/{id}/
        - Delete Table: DELETE /api/tables/{id}/
        - Search Table: GET /api/tables/search_by_name/?name=nameToSearch
    """

    queryset = Table.objects.all()
    serializer_class = TableSerializer

    @action(detail=False, methods=['get'])
    def search_by_name(self, request):
        table_name = request.query_params.get('name', '')
        tables = Table.objects.filter(name__icontains=table_name)
        serializer = self.get_serializer(tables, many=True)
        return Response(serializer.data)


class ColumnViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Column instances.

    Endpoints:
        - List Columns: GET /api/columns/
        - Retrieve Column: GET /api/columns/{id}/
        - Create Column: POST /api/columns/
        - Update Column: PUT /api/columns/{id}/
        - Delete Column: DELETE /api/columns/{id}/
    """

    queryset = Column.objects.all()
    serializer_class = ColumnSerializer
