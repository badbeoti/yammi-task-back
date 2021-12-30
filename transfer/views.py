from rest_framework.generics import ListAPIView
from django.db.models import Q

from yammiback.models import MyUser

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Transfer
from .serializers import TransferSerializer, AirdropTransferSerializer


class AllTransactions(ListAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(Q(id_sender=request.user.id) | Q(id_receiver=request.user.id))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAdminUser])
def airdrop(request):
    newData = request.data.copy()
    newData['id_sender'] = str(request.user.id)

    print(newData)

    create_serializer = AirdropTransferSerializer(data=newData)

    if create_serializer.is_valid():
        receiver = MyUser.objects.get(id=newData['id_receiver'])

        receiver.balance += int(request.data['amount'])

        receiver.save()

        transfer_obj = create_serializer.save()

        read_serializer = AirdropTransferSerializer(transfer_obj)

        return Response(read_serializer.data, status=201)

    # If the users POST data is not valid, return a 400 response with an error message
    return Response(create_serializer.errors, status=400)


@api_view(['POST'])
def send(request):
    create_serializer = TransferSerializer(data=request.data)

    if create_serializer.is_valid():
        sender = MyUser.objects.get(id=request.data['id_sender'])
        receiver = MyUser.objects.get(id=request.data['id_receiver'])

        if sender.balance < int(request.data['amount']):
            return Response(create_serializer.errors, status=403)

        receiver.balance += int(request.data['amount'])
        sender.balance -= int(request.data['amount'])

        receiver.save()
        sender.save()

        transfer_obj = create_serializer.save()

        read_serializer = TransferSerializer(transfer_obj)

        return Response(read_serializer.data, status=201)

    # If the users POST data is not valid, return a 400 response with an error message
    return Response(create_serializer.errors, status=400)