from rest_framework import serializers
from ..models.commerce import Commerce
from ..models.category import Category

class CommerceSerializer(serializers.Serializer):
    id = serializers.UUIDField(format='hex_verbose', required=False)
    merchant_name = serializers.CharField(max_length=255)
    merchant_logo = serializers.URLField(required=False)
    category = serializers.UUIDField(format='hex_verbose')

    def create(self, validated_data):
        category_id = validated_data.pop('category')
        validated_data['category'] = Category.objects(id=category_id).first()
        return Commerce(**validated_data)

    def update(self, instance, validated_data):
        instance.merchant_name = validated_data.get('merchant_name', instance.merchant_name)
        instance.merchant_logo = validated_data.get('merchant_logo', instance.merchant_logo)
        category_id = validated_data.get('category')
        if category_id:
            instance.category = Category.objects(id=category_id).first()
        instance.save()
        return instance