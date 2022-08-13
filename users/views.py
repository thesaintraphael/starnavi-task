from rest_framework import generics
from rest_framework.response import Response

from .models import User
from .serializers import RegistrationSerializer, VerifyEmailSerializer
from mainapp.api.permissions import NotAuthenticated


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (NotAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(is_active=False)


class VerifyEmailAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = VerifyEmailSerializer
    permission_classes = (NotAuthenticated,)

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data["email"])
        user.is_active = True
        user.activation_code = ""
        user.save()

        return Response(
            {"message": "Email verified successfully.", "tokens": user.tokens},
            status=200,
        )
