from django.urls import path, include
from doors.views import DoorListAPIView, SeriesListAPIView

app_name = 'doors'

urlpatterns = [
    path('doors/', DoorListAPIView.as_view(), name='door-list'),
    path('series/', SeriesListAPIView.as_view(), name='series-list'),
]