from django.urls import path

from doors.views import MainPageDoorsAPIView, DetailViewDoorsAPIView, ListViewDoorsAPIView, ListFiltersAPIView, \
    DoorFiltersView

urlpatterns = [
    path('doors/popular/', MainPageDoorsAPIView.as_view(), name='main-page-door-list'),
    path('doors/', ListViewDoorsAPIView.as_view(), name='door-list'),
    path('doors/<uuid:pk>/', DetailViewDoorsAPIView.as_view(), name='door-detail'),
    path('doors/filter', DoorFiltersView.as_view(), name='door-filters'),

    path('filters/', ListFiltersAPIView.as_view(), name='filter-list'),

]
