from rest_framework import serializers
from ..models.category import Category

class CategorySerializer(serializers.Serializer):
    id = serializers.UUIDField(format='hex_verbose', required=False)
    name = serializers.CharField(max_length=255)
    type = serializers.ChoiceField(choices=['expense', 'income'])

    def create(self, validated_data):
        return Category(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance