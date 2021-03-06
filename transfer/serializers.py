from rest_framework import serializers
from .models import Transfer


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('id', 'creation_date', 'id_sender', 'id_receiver', 'amount')


class AirdropTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('id', 'creation_date', 'id_sender', 'id_receiver', 'amount')
