from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User
from .utils import UserCodeUtil
from mainapp.api.utils import SerializerUtil, EmailUtil


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, min_length=6
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
        )

    def validate(self, attrs):
        users = User.objects.filter(email=attrs["email"])

        if users.exists():
            if users.first().is_active:
                raise serializers.ValidationError(
                    {"email": "Email is already in use."}, code=400
                )
            else:
                users.first().delete()

        SerializerUtil.validate_password(attrs["password"])
        SerializerUtil.required(attrs.get("first_name"), "first_name")

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.activation_code = UserCodeUtil.genearte_act_code()
        user.save()

        EmailUtil(
            subject="Email Verification",
            message=f"Code: {user.activation_code}",
            receivers=(user.email,),
        ).send_in_thread()

        return user


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_["tokens"] = self.user.tokens

        return repr_

    def validate(self, attrs):
        users = User.objects.filter(username=attrs["username"])

        if users.exists():
            user = users.first()
            if user.is_active and user.check_password(attrs["password"]):
                self.user = user
                return attrs

        raise AuthenticationFailed(
            "Invalid credentials or account is not active", code=401
        )


class LogoutSerializer(serializers.Serializer):

    refresh_token = serializers.CharField()

    def validate(self, attrs):
        try:
            token = RefreshToken(attrs["refresh_token"])
            token.blacklist()
        except TokenError as e:
            raise AuthenticationFailed(
                detail="Invalid or expired token", code=400
            ) from e

        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    activation_code = serializers.CharField(max_length=6)
    email = serializers.EmailField()

    def validate(self, attrs):

        users = User.objects.filter(email=attrs["email"])
        if users.exists():
            user = users.first()
            if not user.is_active and user.activation_code == attrs["activation_code"]:
                attrs["activation_code"] = ""
                return attrs

        raise AuthenticationFailed(detail="Wrong email or code provided", code=401)
