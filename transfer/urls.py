from django.urls import path
from .views import airdrop, transfer

urlpatterns = [
    path("airdrop/", airdrop),
    path("transfer/", transfer)
]
