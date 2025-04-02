from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserSerializer, NoteCreateSerializer, NoteRetrieveSerializer, PhoneOnlyAuthSerializer, PhonePasswordAuthSerializer
from .models import Note

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_notes(request):
    notes = Note.objects.filter(user=request.user)
    serializer = NoteRetrieveSerializer(notes, many=True)
    return Response(serializer.data)

def generate_audio_url(text):
    return f"https://example.com/audio/{hash(text)}.mp3"