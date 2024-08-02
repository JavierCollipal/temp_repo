from rest_framework import serializers
from temp_repo.models.commerce import Commerce

class CommerceSerializer(serializers.Serializer):
    merchant_name = serializers.CharField(max_length=255)
    merchant_logo = serializers.URLField()
    category = serializers.CharField()