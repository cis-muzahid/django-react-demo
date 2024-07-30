from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import serializers
from .models import DummyData, CustomUser


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer handles the validation and creation of new user instances
    during registration. It ensures that required fields are provided and 
    processes the password securely.

    Attributes:
        Meta (class): Defines the model and fields to be used by the serializer.
    """

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        """
        Create and return a new user instance.

        This method uses the validated data to create a new user with the 
        specified email, password, first name, and last name. The password
        is handled securely using the `create_user` method to ensure proper 
        hashing.

        Args:
            validated_data (dict): The validated data from the serializer.

        Returns:
            CustomUser: The newly created user instance.
        """
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    This serializer validates the email and password provided by the user
    during login. It does not handle user creation or password hashing.

    Attributes:
        email (EmailField): The user's email address.
        password (CharField): The user's password.
    """
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class VerifyEmailSerializer(serializers.Serializer):
    """
    Serializer for email verification.

    This serializer validates the email address and OTP code provided
    for email verification. It ensures that both fields are properly 
    formatted.

    Attributes:
        email (EmailField): The user's email address.
        otp_code (CharField): The one-time password (OTP) code for verification.
    """
    
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

class TokenSerializer(serializers.Serializer):
    """
    Serializer for handling tokens.

    This serializer validates the token provided in the request. It is used
    to ensure that a token is properly formatted.

    Attributes:
        token (CharField): The token string.
    """
    
    token = serializers.CharField()

class DummyDataSerializer(serializers.ModelSerializer):
    """
    Serializer for dummy data records.

    This serializer is used to validate and serialize dummy data entries,
    including basic user information.

    Attributes:
        Meta (class): Defines the model and fields to be used by the serializer.
    """
    
    class Meta:
        model = DummyData
        fields = ['id', 'first_name', 'last_name', 'phone']
