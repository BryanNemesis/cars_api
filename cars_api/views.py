from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import Car
from .serializers import CarSerializer, PopularCarSerializer


@api_view(['GET', 'POST'])
def car_list_and_create_view(request):
    if request.method == 'GET':
        qs = Car.objects.all()
        serializer = CarSerializer(qs, many=True)
        return Response(serializer.data, status=200)

    elif request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def car_delete_view(request, car_id):
    qs = Car.objects.filter(pk=car_id)
    if qs.exists():
        car = qs.first()
        serializer = CarSerializer(car)
        car.delete()
        return Response(serializer.data, status=200)
    else:
        return Response({}, status=404)


@api_view(['GET'])
def popular_car_list_view(request):
    qs = Car.objects.all()
    qs = qs.annotate(rating_count=Count('ratings'))
    qs = qs.order_by('-rating_count')
    serializer = PopularCarSerializer(qs, many=True)
    return Response(serializer.data, status=200)
