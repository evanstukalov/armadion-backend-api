from django.urls import path
from doors.views import DoorListAPIView

app_name = 'doors'

urlpatterns = [
    path('doors/', DoorListAPIView.as_view(), name='door-list'),
]