from rest_framework import serializers

from twitter.models import Tweet


class TweetSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=280)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data: dict):
        author = self.context["request"].user
        return Tweet.objects.create(author=author, **validated_data)
