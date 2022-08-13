from rest_framework import generics

from .models import User
from .serializers import RegistrationSerializer
from mainapp.api.permissions import NotAuthenticated


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (NotAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(is_active=False)
