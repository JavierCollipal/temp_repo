from rest_framework import serializers
from ..models.keyword import Keyword
from ..models.commerce import Commerce

class KeywordSerializer(serializers.Serializer):
    id = serializers.UUIDField(format='hex_verbose', required=False)
    keyword = serializers.CharField(max_length=255)
    merchant_id = serializers.UUIDField(format='hex_verbose')

    def create(self, validated_data):
        merchant_id = validated_data.pop('merchant_id')
        validated_data['merchant_id'] = Commerce.objects(id=merchant_id).first()
        return Keyword(**validated_data)

    def update(self, instance, validated_data):
        instance.keyword = validated_data.get('keyword', instance.keyword)
        merchant_id = validated_data.get('merchant_id')
        if merchant_id:
            instance.merchant_id = Commerce.objects(id=merchant_id).first()
        instance.save()
        return instance