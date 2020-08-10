from django.shortcuts import render
from django.http import HttpResponse
from .serializers import VehicleSerializer
from .models import Vehicle
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from django.http.response import JsonResponse


class vehicle_view(generics.GenericAPIView):
    serializer_class = VehicleSerializer
    def post(self,request):
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):

        vehicle = Vehicle.objects.all()
        vehicle_serializer =VehicleSerializer(vehicle, many=True)
        return JsonResponse(vehicle_serializer.data, safe=False)

