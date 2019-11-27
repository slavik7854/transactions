from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from decimal import Decimal

from .models import Payment, Account
from .serializers import PaymentSerializer, AccountSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @swagger_auto_schema(
        responses={
            201: PaymentSerializer,
            400: "Validation error"
        }
    )
    def get_queryset(self):
        return Payment.objects.all()


        # Response({'payments': Payment.objects.all()})

    @swagger_auto_schema(
        responses={
            201: PaymentSerializer,
            400: "Validation error"
        }
    )
    def perform_create(self, serz):
        '''
        Payments create

        Create payment instances
        '''
        to_account = Account.objects.get(id=serz.data['to_account'])
        account = self.request.user.account_set.get(
            currency=Account.objects.get(id=serz.data['to_account']).currency)
        account.balance -= Decimal(serz.data['amount'])
        to_account.balance += Decimal(serz.data['amount'])
        account.save(update_fields=['balance'])
        to_account.save(update_fields=['balance'])
        Payment.objects.create(
            account=account,
            amount=Decimal(serz.data['amount']),
            to_account=to_account,
            direction='Outgoing'
        )
        Payment.objects.create(
            account=to_account,
            amount=Decimal(serz.data['amount']),
            from_account=account,
            direction='Incoming'
        )
        return Response(self.serializer_class.data, status=status.HTTP_201_CREATED)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    http_method_names = ['get']