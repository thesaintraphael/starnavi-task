from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response


from .models import User
from .serializers import (
    LogoutSerializer,
    RegistrationSerializer,
    VerifyEmailSerializer,
    LoginSerializer,
    UserActivitySerializer,
)
from mainapp.api.permissions import NotAuthenticated


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (NotAuthenticated,)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        return Response(
            {"message": "Veification email is sent"},
            status=201,
        )


class UserLoginAPIView(generics.GenericAPIView):

    serializer_class = LoginSerializer
    permission_classes = (NotAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=200)


class UserLogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"message": "Logged out successfully"}, status=200)


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


class UserActivityAPIView(generics.GenericAPIView):

    serializer_class = UserActivitySerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):

        users = request.user
        many = False
        if request.user.is_staff:
            many = True
            users = self.get_queryset()

        serializer = self.serializer_class(users, many=many)
        return Response(serializer.data, status=200)
