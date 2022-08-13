from rest_framework import serializers

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