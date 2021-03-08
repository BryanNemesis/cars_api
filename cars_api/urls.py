from django.urls import path

from .views import CarListView

urlpatterns = [
    path('cars/', CarListView),
    ]
