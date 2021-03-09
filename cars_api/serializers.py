from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Avg
import requests

from .models import Car, Rating


def car_exists_validator(values):
    api_url = 'https://vpic.nhtsa.dot.gov/api/vehicles/'
    make, model = values['make'], values['model']

    makes_json = requests.get(f'{api_url}/GetAllMakes?format=json')
    makes = [d['Make_Name'] for d in makes_json.json()['Results']]
    if not make.upper() in makes:
        raise serializers.ValidationError(f'Car make {make} does not exist.')
    
    models_json = requests.get(f'{api_url}/GetModelsForMake/{make}?format=json')
    models = [d['Model_Name'] for d in models_json.json()['Results']]
    if not model in models:
        raise serializers.ValidationError(f'Car model {model} does not exist for make {make}.')


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'avg_rating']
        validators = [
            car_exists_validator,
            UniqueTogetherValidator(
                queryset=Car.objects.all(),
                fields=['make', 'model'],
                message='A car like this already exists in the database.'
            ),
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


class CarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['car', 'rating']

    def validate_rating(self, value):
        if not (isinstance(value, int) and 1 <= value <= 5):
            raise serializers.ValidationError('Rating must be a number from 1 to 5.')
        return value