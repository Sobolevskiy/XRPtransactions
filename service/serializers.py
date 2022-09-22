from rest_framework import serializers

from service import models


class TransactionSerializer(serializers.ModelSerializer):
    destination = serializers.SlugRelatedField(slug_field='address', queryset=models.AccountAddress.objects.all())

    class Meta:
        model = models.Transactions
        fields = "__all__"


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccountAddress
        fields = ("address",)
