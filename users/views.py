from rest_framework import generics
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication
)
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserSerializer, DisplayUserSerializer


class CreateUserAPIView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class RetrieveUpdateUserAPIView(generics.RetrieveUpdateAPIView):
    """Retrieve and update user view"""
    serializer_class = DisplayUserSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
