from django.urls import path

from .views import car_list_and_create_view, car_delete_view, popular_car_list_view

urlpatterns = [
    path('cars/', car_list_and_create_view),
    path('cars/<int:car_id>/', car_delete_view),
    path('popular/', popular_car_list_view),
    ]
