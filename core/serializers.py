from . import models
from rest_framework import serializers


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Game
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'name', 
            'description', 
        )


class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Level
        fields = (
            'slug', 
            'name', 
            'created', 
            'last_updated', 
        )


class CharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Character
        fields = (
            'pk', 
            'name', 
            'description', 
            'created', 
            'last_updated',
        )


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Media
        fields = (
            'pk', 
            'name', 
            'description', 
            'created', 
            'last_updated', 
            'url', 
            'file', 
            'type', 
        )


class MechanicSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Mechanic
        fields = (
            'pk', 
            'name', 
            'description', 
            'created', 
            'last_updated',
        )


