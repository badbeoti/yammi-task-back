from django.urls import path
from .views import airdrop, send, AllTransactions

urlpatterns = [
    path("airdrop/", airdrop),
    path("send/", send),
    path('transactions/', AllTransactions.as_view(), name='transactions')
]
