from django.urls import path, include
from doors.views import DoorListAPIView

app_name = 'doors'

urlpatterns = [
    path('', DoorListAPIView.as_view(), name='door-list'),
]