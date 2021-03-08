from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import Car
from .serializers import CarSerializer


@api_view(['GET'])
def CarListView(request):
    qs = Car.objects.all()
    serializer = CarSerializer(qs, many=True)

    return Response(serializer.data, status=200)