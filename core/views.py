from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from core.models import Messages
from rest_framework import permissions, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, MessagesSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessagesViewSet(viewsets.ModelViewSet):
   
    permission_classes = (permissions.AllowAny,)
    
    """
    API endpoint that allows groups to be viewed or edited.
    """

    def post(self, request):
            
        serializer = MessagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        message = self.get_object(pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
  
    
    