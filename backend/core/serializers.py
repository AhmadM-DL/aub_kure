from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Note, Mood

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class PhonePasswordAuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(phone_number=data['phone_number'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user.get_tokens_for_user()

class PhoneOnlyAuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    
    def validate(self, data):
        try:
            user = User.objects.get(phone_number=data['phone_number'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        return user.get_tokens_for_user()

class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['text']

class MoodSerializer(serializers.ModelSerializer):
    note_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Mood
        fields = ['note_id', 'mood', 'created_at']
        extra_kwargs = {'created_at': {'read_only': True}}

class NoteRetrieveSerializer(serializers.ModelSerializer):
    moods = MoodSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = ['text', 'audio_url', 'created_at', 'is_suicidal', 'moods']

class MarkSuicidalSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Note
        fields = ['id']