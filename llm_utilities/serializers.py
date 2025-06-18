from rest_framework import serializers

class UserInputSerializer(serializers.Serializer):
    user_input = serializers.CharField(required=True)

class TaskConfirmationSerializer(serializers.Serializer):
    tasks = serializers.ListField(child=serializers.DictField(), required=True)