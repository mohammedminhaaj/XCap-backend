from rest_framework.serializers import Serializer, CharField, EmailField, ModelSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from xcap.utils import SERVER_ERROR_MESSAGE
import random
import secrets


class CredentialManager():
    """
    Manager class for user-related actions that involve username and password.
    """

    def validate_user_credentials(self, username, password):
        """
        Validate user credentials and return the user instance if successful, otherwise raise an error.
        """
        try:
            user = User.objects.get(username=username)
            if not check_password(password, user.password):
                raise AuthenticationFailed()
            return user
        except (User.DoesNotExist, AuthenticationFailed):
            raise AuthenticationFailed("Invalid Credentials")
        except Exception:
            raise AuthenticationFailed(SERVER_ERROR_MESSAGE)

    def get_token_response(self, user):
        """
        Generate an authentication token for the user and return a response structure.
        """
        token, _ = Token.objects.get_or_create(user=user)
        return {"auth_token": token.key}


class LoginSerializer(Serializer, CredentialManager):
    username = CharField(min_length=6, max_length=128)
    password = CharField(min_length=6, max_length=128)
    """
    Serializer for user login, inheriting from Serializer and CredentialManager.
    """

    def validate(self, data):
        """
        Validate the login credentials and return a successful response with the auth token.
        """
        user = self.validate_user_credentials(
            data['username'], data['password'])
        return self.get_token_response(user)


class SignupSerializer(ModelSerializer, CredentialManager):
    """
    ModelSerializer for user signup.
    """
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(**validated_data)

        user.set_password(password)
        user.save()

        return self.get_token_response(user)
        

class ForgotPasswordSerializer(Serializer):
    """
    Serializer for handling forgotten password requests via email.
    """
    username = CharField(min_length=6, max_length=128)
    email = EmailField()

    def create(self, validated_data):

        user = User.objects.get(**validated_data)
        password = secrets.token_urlsafe(8)
        user.password = make_password(password)
        user.save(update_fields=["password"])
        print(f"Password for {user.username} is {password}")
        return user
