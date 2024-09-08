from rest_framework.request import Request
from rest_framework.decorators import api_view
from .serializer import LoginSerializer, SignupSerializer, ForgotPasswordSerializer
from xcap.utils import response_structure, SERVER_ERROR_MESSAGE
from rest_framework import status

# Create your views here.


@api_view(['POST'])
def login(request: Request):

    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return response_structure("Login Successful", status.HTTP_200_OK, serializer.validated_data)
    return response_structure(SERVER_ERROR_MESSAGE, status.HTTP_400_BAD_REQUEST, serializer.errors)


@api_view(['POST'])
def signup(request: Request):

    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user_data = serializer.save()
        return response_structure("Account Created Successfully", status.HTTP_201_CREATED, user_data)
    return response_structure(SERVER_ERROR_MESSAGE, status.HTTP_400_BAD_REQUEST, serializer.errors)


@api_view(['POST'])
def forgot_password(request: Request):

    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
        except Exception:
            pass
        return response_structure("Email Sent", status.HTTP_200_OK)
    return response_structure(SERVER_ERROR_MESSAGE, status.HTTP_400_BAD_REQUEST, serializer.errors)
