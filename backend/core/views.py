from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserSerializer
from .serializers import NoteCreateSerializer, NoteRetrieveSerializer, MarkSuicidalSerializer
from .serializers import PhoneOnlyAuthSerializer, PhonePasswordAuthSerializer
from .serializers import MoodSerializer
from .models import Note, Mood

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_with_password(request):
    serializer = PhonePasswordAuthSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_with_phone(request):
    serializer = PhoneOnlyAuthSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note(request):
    serializer = NoteCreateSerializer(data=request.data)
    if serializer.is_valid():
        note = serializer.save(user=request.user, audio_url=generate_audio_url(serializer.validated_data['text']))
        return Response({'id': note.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_note_as_suicidal(request):
    serializer = MarkSuicidalSerializer(data=request.data)
    if serializer.is_valid():
        try:
            print(serializer.validated_data)
            id = serializer.validated_data['id']
            note = Note.objects.get(id=id, user=request.user)
        except Note.DoesNotExist:
            return Response({'error': 'Note not found or access denied.'}, status=status.HTTP_404_NOT_FOUND)
        note.is_suicidal = True
        note.save()
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_notes(request):
    notes = Note.objects.filter(user=request.user).prefetch_related('moods') 
    serializer = NoteRetrieveSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_mood(request):
    serializer = MoodSerializer(data=request.data)
    if serializer.is_valid():
        note_id = serializer.validated_data.pop('note_id')
        try:
            note = Note.objects.get(id=note_id, user=request.user)
        except Note.DoesNotExist:
            return Response({'error': 'Note not found or access denied.'}, status=status.HTTP_404_NOT_FOUND)
        Mood.objects.create(note=note, **serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def generate_audio_url(text):
    return f"https://example.com/audio/{hash(text)}.mp3"