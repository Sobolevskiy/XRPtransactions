from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins

from service import models, serializers


class TransactionsViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = models.Transactions.objects.all()
    serializer_class = serializers.TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['hash', 'ledger_index']


class AccountsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.AccountAddress.objects.all()
    serializer_class = serializers.AccountsSerializer
