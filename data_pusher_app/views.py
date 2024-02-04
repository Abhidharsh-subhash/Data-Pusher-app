from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import accountserializer, DestinationSerializer
from .models import Account, Destination
import secrets
import string
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

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

    def get(self, request):
        id = request.data.get('accountid')
        if id:
            account = get_object_or_404(Account, id=id)
            serializer = self.serializer_class(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            accounts = Account.objects.all()
            serializer = self.serializer_class(accounts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        id = request.data.get('accountid')
        account = get_object_or_404(Account, id=id)
        account.delete()

        response = {
            'status': 204,
            'message': 'Account deleted successfully'
        }
        return Response(data=response, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request):
        id = request.data.get('id')
        account = get_object_or_404(Account, id=id)
        breakpoint()
        fields = request.data.keys()
        # for i in fields:
        #     Account.objects.filter(id=id).update(i=request.data[i])
        for field in fields:
            if hasattr(account, field):
                setattr(account, field, request.data.get(field))
        account.save()
        response = {
            'status': 200,
            'message': 'Account updated successfully'
        }
        return Response(data=response, status=status.HTTP_200_OK)


class destinationview(GenericAPIView):
    serializer_class = DestinationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 201,
                'message': 'Destination created successfully'
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        pass

    def delete(self, request):
        pass

    def patch(self, request):
        pass
