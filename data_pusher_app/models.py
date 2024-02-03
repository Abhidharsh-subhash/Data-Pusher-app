from django.db import models

# Create your models here.

class Account(models.Model):    
    email = models.EmailField(unique=True, blank=False)
    account_id = models.CharField(max_length=255, unique=True)
    account_name = models.CharField(max_length=255, blank=False, null=False)
    app_secret_token = models.CharField(max_length=255, unique=True, blank=False, null=False)
    website = models.URLField(blank=True)
