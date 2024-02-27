from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import GameSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from user.models import Game
from rest_framework import status


class GameView(APIView):
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
