from django.urls import path
from .views import airdrop, send

urlpatterns = [
    path("airdrop/", airdrop),
    path("send/", send)
]
