from django.urls import include, path
from rest_framework.routers import DefaultRouter

from sheetdata.views import SheetView

router = DefaultRouter()

urlpatterns = [
    path("data/", SheetView.as_view(), name="sheet-view"),
    path("", include(router.urls)),
]
