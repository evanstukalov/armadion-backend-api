from django.urls import path

from doors.views import MainPageDoorsAPIView, DetailViewDoorsAPIView, SimilarDoorsAPIView, ListViewDoorsAPIView

urlpatterns = [
    path('main-page-doors/', MainPageDoorsAPIView.as_view(), name='main-page-door-list'),
    path('doors/', ListViewDoorsAPIView.as_view(), name='door-list'),
    path('doors/<int:pk>/', DetailViewDoorsAPIView.as_view(), name='door-detail'),
    path('doors/<int:pk>/similar-doors/', SimilarDoorsAPIView.as_view(), name='similar-products'),
]