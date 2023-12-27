from django.urls import path
from .views import AirplaneListCreateView, AirplaneListView

urlpatterns = [
    path('airplanes/', AirplaneListCreateView.as_view(), name='airplane-list-create'),
    path('airplanesList/', AirplaneListView.as_view(), name='airplane-list-create'),
]