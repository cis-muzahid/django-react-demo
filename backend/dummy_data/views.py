from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, VerifyEmailSerializer
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .models import DummyData
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import DummyDataSerializer
from rest_framework import generics,status,views,permissions
from dummy_data.utils import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    API view for registering a new user.

    This view allows new users to register by providing their details. 
    It uses the `RegisterSerializer` to validate and save user data, 
    and returns a JSON response with the user information and JWT tokens.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """
        Save the new user instance and generate authentication tokens.

        This method saves the user instance, activates the user account,
        and generates a JWT refresh token and an access token.

        Args:
            serializer (RegisterSerializer): The serializer instance 
                containing validated user data.

        Returns:
            dict: A dictionary containing user information and authentication tokens.
        """
        user = serializer.save()
        user.is_active = True
        user.save()
        
        refresh = RefreshToken.for_user(user)
        return {
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_active': user.is_active,
            },
            'refresh': str(refresh),
            'api_token': str(refresh.access_token),
        }

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to register a new user.

        Validates the request data using the serializer, creates a new user,
        and returns the user details and JWT tokens in the response.

        Args:
            request (Request): The request instance containing user input data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: An HTTP response containing user details and tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = self.perform_create(serializer)
        return Response(response_data, status=status.HTTP_201_CREATED)



class LoginView(APIView):
    """
    API view for user login.

    This view handles user authentication by verifying credentials provided
    in the request. Upon successful authentication, it returns JWT tokens for
    client access.
    """
    
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST requests to authenticate a user.

        This method validates the user's email and password, authenticates the
        user, and returns a response with a JWT refresh token and access token.
        
        Args:
            request (Request): The HTTP request instance containing login data.
            
        Returns:
            Response: An HTTP response containing authentication tokens if
            successful, or an error message if authentication fails.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                if not user.is_active:
                    return Response({'error': 'User account is disabled.'}, status=status.HTTP_400_BAD_REQUEST)
                
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'api_token': str(refresh.access_token),
                })
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyTokenView(APIView):
    """
    API view for verifying JWT access tokens.

    This view handles the verification of JWT access tokens to ensure that
    the token provided by the user is valid and has not expired.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST requests to verify a JWT access token.

        This method checks if a token is provided in the request data, validates
        it using the `AccessToken` class, and returns a response indicating
        whether the token is valid or invalid.

        Args:
            request (Request): The HTTP request instance containing the token
            in the request data.

        Returns:
            Response: An HTTP response indicating the token's validity status:
            - A success message with HTTP 200 status if the token is valid.
            - An error message with HTTP 400 status if the token is missing or invalid.
        """
        token = request.data.get('api_token')
        if not token:
            return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            AccessToken(token)
            return Response({'message': 'Token is valid.'}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        
class DummyDataView(APIView):
    """
    API view for retrieving dummy data.

    This view is used to fetch a list of dummy data records from the database.
    It requires the user to be authenticated to access the data.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Handle GET requests to retrieve dummy data records.

        This method fetches all dummy data entries from the database, serializes
        the data using `DummyDataSerializer`, and returns the serialized data
        in the HTTP response.

        Args:
            request (Request): The HTTP request instance used to process the
            GET request.

        Returns:
            Response: An HTTP response containing the serialized dummy data
            records with a status code of 200 OK.
        """
        users = DummyData.objects.all()
        serializer = DummyDataSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

