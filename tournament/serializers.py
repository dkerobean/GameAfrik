from rest_framework import serializers
from user.models import Game, Tournament


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
