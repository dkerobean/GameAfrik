from rest_framework import serializers
from user.models import Game, Tournament, Profile


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar', 'username']


class TournamentSerializer(serializers.ModelSerializer):
    game = GameSerializer()
    host = ProfileSerializer()
    participants = ProfileSerializer(many=True)

    class Meta:
        model = Tournament
        fields = '__all__'
