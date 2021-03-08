from rest_framework import serializers
from django.db.models import Avg

from .models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['make', 'model', 'average_rating']

    average_rating = serializers.SerializerMethodField(read_only=True)

    def get_average_rating(self, obj):
        return obj.ratings.all().aggregate(Avg('rating'))['rating__avg']
