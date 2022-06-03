from django.urls import path
from .views import countParkSpaceView

app_name = "countparkspace"

urlpatterns = [
    path("", countParkSpaceView),
]