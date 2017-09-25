from . import models
from . import serializers
from rest_framework import viewsets, permissions


class GameViewSet(viewsets.ModelViewSet):
    """ViewSet for the Game class"""

    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer
    permission_classes = [permissions.IsAuthenticated]


class LevelViewSet(viewsets.ModelViewSet):
    """ViewSet for the Level class"""

    queryset = models.Level.objects.all()
    serializer_class = serializers.LevelSerializer
    permission_classes = [permissions.IsAuthenticated]


class CharacterViewSet(viewsets.ModelViewSet):
    """ViewSet for the Character class"""

    queryset = models.Character.objects.all()
    serializer_class = serializers.CharacterSerializer
    permission_classes = [permissions.IsAuthenticated]


class MediaViewSet(viewsets.ModelViewSet):
    """ViewSet for the Media class"""

    queryset = models.Media.objects.all()
    serializer_class = serializers.MediaSerializer
    permission_classes = [permissions.IsAuthenticated]


class MechanicViewSet(viewsets.ModelViewSet):
    """ViewSet for the Mechanic class"""

    queryset = models.Mechanic.objects.all()
    serializer_class = serializers.MechanicSerializer
    permission_classes = [permissions.IsAuthenticated]


