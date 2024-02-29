from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import GameSerializer, TournamentSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from user.models import Game, Tournament
from rest_framework import status
from rest_framework.exceptions import PermissionDenied


class GameView(APIView):
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TournamentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tournaments = Tournament.objects.all()
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.role == 'host':
            raise PermissionDenied('Only hosts can create tournaments')

        serializer = TournamentSerializer(data=request.data)
        if serializer.is_valid():
            # assign host to tournament
            serializer.validated_data['host'] = request.user.profile
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        tournament = get_object_or_404(Tournament, uuid=pk)

        # Check if the user is the host of the tournament
        if request.user.profile != tournament.host:
            raise PermissionDenied('You do not have permission to perform this action')

        serializer = TournamentSerializer(tournament, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tournament = get_object_or_404(Tournament, uuid=pk)

        # Check if the user is the host of the tournament
        if request.user.profile != tournament.host:
            raise PermissionDenied("You do not have permission to perform this action.")

        tournament.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





