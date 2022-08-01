# Create your views here.
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserSerializer


class UserList(APIView):

    def get(self, request, format=None):
        users = User.objects.all()
        return Response([UserSerializer(user).data for user in users])

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        return Response(UserSerializer(user).data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(request)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
