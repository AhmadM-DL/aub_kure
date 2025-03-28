from rest_framework import serializers
from .models import User, Note, Mood

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['text']

class NoteRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['text', 'audio_url', 'created_at', 'is_suicidal']
