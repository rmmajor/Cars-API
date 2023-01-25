from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class RegistrationSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField()
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirmed_password"]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirmed_password"]:
            raise ValidationError("Entered passwords mismatched")

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("confirmed_password")
        return User.objects.create_user(**validated_data)
