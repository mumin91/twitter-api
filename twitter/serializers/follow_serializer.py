from rest_framework import serializers


class FollowSerializer(serializers.Serializer):
    target_user_id = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
