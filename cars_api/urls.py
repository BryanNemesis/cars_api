from django.urls import path

from .views import car_list_and_create_view, car_delete_view, car_rate_view, popular_car_list_view

urlpatterns = [
    path('cars/', car_list_and_create_view, name='car-list-and-create'),
    path('cars/<int:car_id>/', car_delete_view, name='car-delete'),
    path('rate/', car_rate_view, name='car-rate'),
    path('popular/', popular_car_list_view, name='popular-car-list'),
    ]
