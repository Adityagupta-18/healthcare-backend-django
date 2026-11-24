from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate



class RegisterSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value.lower()

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Name cannot be empty."
            )

        return value

    def create(self, validated_data):
        name = validated_data.pop('name')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        name_parts = name.split(maxsplit=1)

        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        return user





class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        user = authenticate(
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        attrs['user'] = user
        return attrs
