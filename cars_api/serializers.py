from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Avg

from .models import Car



def car_exists_validator(values):
    # TODO: add checking against https://vpic.nhtsa.dot.gov/api/ if such car exists
    car_exists = True
    print(values['make'], values['model'])
    if not car_exists:
        raise serializers.ValidationError('A car like this does not exist.')


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'avg_rating']
        validators = [
            UniqueTogetherValidator(
                queryset=Car.objects.all(),
                fields=['make', 'model'],
                message='A car like this already exists in the database.'
            ),
            car_exists_validator
        ]

    avg_rating = serializers.SerializerMethodField(read_only=True)

    def get_avg_rating(self, obj):
        return obj.ratings.all().aggregate(Avg('rating'))['rating__avg']


class PopularCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'rates_number']

    rates_number = serializers.SerializerMethodField(read_only=True)

    def get_rates_number(self, obj):
        return obj.ratings.count()
