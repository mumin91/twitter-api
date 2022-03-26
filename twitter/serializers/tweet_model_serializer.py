from rest_framework import serializers

from twitter.models import Tweet


class TweetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = "__all__"
