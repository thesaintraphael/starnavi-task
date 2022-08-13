from rest_framework import generics
from rest_framework import permissions

from .models import User
from .serializers import RegistrationSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.save(is_active=False)
