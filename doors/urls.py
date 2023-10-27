from django.urls import path

from doors.views import MainPageDoorsAPIView, DetailViewDoorsAPIView

urlpatterns = [
    path('main-page-doors/', MainPageDoorsAPIView.as_view(), name='main-page-door-list'),
    path('doors/<int:pk>/', DetailViewDoorsAPIView.as_view(), name='door_detail'),
]