from rest_framework.request import Request
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializer import LoginSerializer, SignupSerializer, ForgotPasswordSerializer, ChangeEmailSerializer, ChangePasswordSerializer
from xcap.utils import response_structure, SERVER_ERROR_MESSAGE, SUCCESS_MESSAGE
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.


@api_view(['POST'])
def login(request: Request):
    """Function to handle login flow"""
    # Create serializer instance
    serializer = LoginSerializer(data=request.data)
    # Check if the username and password is valid
    if serializer.is_valid():
        return response_structure("Login Successful", status.HTTP_200_OK, serializer.validated_data)
    return response_structure(SERVER_ERROR_MESSAGE, status.HTTP_400_BAD_REQUEST, serializer.errors)


@api_view(['POST'])
def signup(request: Request):
    """Serializer to handle sign up flow"""
    # Create serializer instance
    serializer = SignupSerializer(data=request.data)
    # Check if user data is valid
    if serializer.is_valid():
        # Create the user
        user_data = serializer.save()
        return response_structure("Account Created Successfully", status.HTTP_201_CREATED, user_data)
    return response_structure(SERVER_ERROR_MESSAGE, status.HTTP_400_BAD_REQUEST, serializer.errors)


@api_view(['POST'])
def forgot_password(request: Request):
    """Function to handle forgot password flow"""
    # Create serializer instance
    serializer = ForgotPasswordSerializer(data=request.data)
    # Check if the data is valid
    if serializer.is_valid():
        try:
            serializer.save()
        except Exception:  # Handle any errors
            pass
        return response_structure("Email Sent", status.HTTP_200_OK)
    return response_structure(SERVER_ERROR_MESSAGE, status.HTTP_400_BAD_REQUEST, serializer.errors)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_email(request: Request):
    """Function to handle email change request"""
    # Create serializer instance
    serializer = ChangeEmailSerializer(request.user, data=request.data)
    # Check if the data is valid
    if serializer.is_valid():
        # Update the email
        serializer.save()
        return response_structure("Email Updated", status.HTTP_200_OK)
    return response_structure(SERVER_ERROR_MESSAGE, status.HTTP_400_BAD_REQUEST, serializer.errors)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request: Request):
    """Function to handle change password request"""
    # Create serializer instance
    serializer = ChangePasswordSerializer(request.user, data=request.data)
    # Check if the data is valid
    if serializer.is_valid():
        # Change the password
        serializer.save()
        return response_structure("Password Updated", status.HTTP_200_OK)
    return response_structure(SERVER_ERROR_MESSAGE, status.HTTP_400_BAD_REQUEST, serializer.errors)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request: Request):
    """Function to get user details such as username and password"""
    return response_structure(SUCCESS_MESSAGE, status.HTTP_200_OK, {"username": request.user.username, "email": request.user.email})
