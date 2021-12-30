from yammiback.models import MyUser

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Transfer
from .serializers import TransferSerializer, AirdropTransferSerializer


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
def transfer(request):
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