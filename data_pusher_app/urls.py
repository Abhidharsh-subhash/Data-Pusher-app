from django.urls import path
from .import views

urlpatterns = [
    path('accountview/', views.accountView.as_view(), name='accountview'),
]
