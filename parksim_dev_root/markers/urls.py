from django.urls import path
from .views import MarkersMapView

app_name = "markers"

urlpatterns = [
    path("", MarkersMapView.as_view()),
]