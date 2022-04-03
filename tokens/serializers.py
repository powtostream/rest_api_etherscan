from rest_framework import serializers
from .models import Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["owner", "unique_hash", "tx_hash", "media_url"]


class PostSerializer(serializers.Serializer):
    media_url = serializers.URLField()
    owner = serializers.CharField(max_length=42, min_length=42)
