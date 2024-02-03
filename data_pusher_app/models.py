from django.db import models

# Create your models here.


class Account(models.Model):
    email = models.EmailField(unique=True, blank=False)
    account_id = models.CharField(max_length=255, unique=True)
    account_name = models.CharField(max_length=255, blank=False, null=False)
    app_secret_token = models.CharField(
        max_length=255, unique=True, blank=False, null=False)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.email


class Destination(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='account_reference')
    url = models.URLField(unique=True)
    http_method = models.CharField(max_length=10)
    headers = models.JSONField()

    def __str__(self):
        return f"Destination - {self.url}"
