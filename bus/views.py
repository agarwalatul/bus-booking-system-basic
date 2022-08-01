# Create your views here.
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bus.models import Bus
from bus.serializer import BusSerializer


class BusList(APIView):

    def get(self, request, format=None):
        users = Bus.objects.all()
        return Response([BusSerializer(user).data for user in users])

    def post(self, request, format=None):
        serializer = BusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class BusDetail(APIView):

    def get_object(self, pk):
        try:
            return Bus.objects.get(pk=pk)

        except Bus.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        bus = self.get_object(pk)
        return Response(BusSerializer(bus).data)

    def put(self, request, pk, format=None):
        bus = self.get_object(pk)
        serializer = BusSerializer(request)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
