from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import accountserializer
from .models import Account
import secrets
import string
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


def generate_random_string(length=30):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string


class accountView(GenericAPIView):
    serializer_class = accountserializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            account_id = serializer.validated_data['account_id']
            account_name = serializer.validated_data['account_name']
            website = serializer.validated_data['website']
            account = Account.objects.create(
                email=email,
                account_id=account_id,
                account_name=account_name,
                website=website
            )
            secret = generate_random_string()
            while Account.objects.filter(app_secret_token=secret).exists():
                secret = generate_random_string()
            account.app_secret_token = secret
            account.save()
            response = {
                'status': 201,
                'message': 'Account created successfully'
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            response = {
                'status': 400,
                'message': 'something went wrong try again'
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
