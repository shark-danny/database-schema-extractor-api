from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TableViewSet, ColumnViewSet, DatabaseViewSet

router = DefaultRouter()
router.register(r"databases", DatabaseViewSet)
router.register(r"tables", TableViewSet)
router.register(r"columns", ColumnViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
