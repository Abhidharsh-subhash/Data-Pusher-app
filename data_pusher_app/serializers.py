from rest_framework import serializers
from .models import Account
from django.core.validators import EmailValidator
from rest_framework.validators import ValidationError

class accountserializer(serializers.ModelSerializer):
    email = serializers.CharField(validators=[EmailValidator()])
    account_id = serializers.CharField()
    account_name = serializers.CharField()
    website = serializers.URLField(allow_blank=True)

    def validate(self, attrs):
        queryset=Account.objects.all()
        email_exist=queryset.filter(email=attrs['email']).exists()
        if not attrs.get('email'):
            raise serializers.ValidationError("email cannot be empty.")
        if not attrs.get('account_id'):
            raise serializers.ValidationError("account_id cannot be empty.")
        if not attrs.get('account_name'):
            raise serializers.ValidationError("account_name cannot be empty.")
        if email_exist:
            raise ValidationError('Email has already been used.')
        return attrs

    class Meta:
        model = Account
        fields = ['email','account_id','account_name','website']