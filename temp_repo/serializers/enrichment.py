from rest_framework import serializers
from ..models.transaction import Transaction
from ..models.commerce import Commerce 
from ..models.category import Category

class EnrichedTransactionSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    description = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateField()
    category_id = serializers.UUIDField(allow_null=True, required=False)
    commerce_id = serializers.UUIDField(allow_null=True, required=False)
    merchant_name = serializers.CharField(max_length=255, allow_null=True, required=False)
    merchant_logo = serializers.URLField(allow_null=True, required=False)

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'description', 'amount', 'date']
