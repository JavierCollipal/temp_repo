from rest_framework import serializers
from ..models.transaction import Transaction

class TransactionSerializer(serializers.Serializer):
    id = serializers.UUIDField(format='hex_verbose', required=False)
    description = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateField()

    def create(self, validated_data):
        return Transaction(**validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance