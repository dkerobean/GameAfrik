from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import GameSerializer, TournamentSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from user.models import Game, Tournament
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import permission_classes


class GameView(APIView):
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TournamentsView(APIView):

    def get(self, request):
        tournaments = Tournament.objects.all()
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
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

    @permission_classes([IsAuthenticated])
    def put(self, request, pk):
        tournament = get_object_or_404(Tournament, uuid=pk)

        # Check if the user is the host of the tournament
        if request.user.profile != tournament.host:
            raise PermissionDenied('You do not have permission to perform this action')  # noqa

        serializer = TournamentSerializer(tournament, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsAuthenticated])
    def delete(self, request, pk):
        tournament = get_object_or_404(Tournament, uuid=pk)

        # Check if the user is the host of the tournament
        if request.user.profile != tournament.host:
            raise PermissionDenied("You do not have permission to perform this action.") # noqa

        tournament.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TournamentView(APIView):
    def get(self, request, pk):
        tournament = get_object_or_404(Tournament, uuid=pk)
        serializer = TournamentSerializer(tournament)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JoinedTournamentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tournaments = Tournament.objects.filter(
            participants=request.user.profile)
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HostedTournamentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tournaments = Tournament.objects.filter(
            host=request.user.profile)
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LeaveTournamentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        tournament = get_object_or_404(Tournament, uuid=pk)
        if request.user.profile in tournament.participants.all():
            tournament.participants.remove(request.user.profile)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You are not registered in this tournament."}, # noqa
                            status=status.HTTP_400_BAD_REQUEST)


class JoinTournamentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        tournament = get_object_or_404(Tournament, uuid=pk)

        # Check if the tournament is already started or finished
        if tournament.status != 'open':
            return Response({"detail": "Cannot join the tournament. It is not open for registration."},  # noqa
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is already a participant
        if request.user.profile in tournament.participants.all():
            return Response({"detail": "You are already registered in this tournament."},  # noqa
                            status=status.HTTP_400_BAD_REQUEST)

        # check available slots for the tournament
        if tournament.number_of_participants == tournament.participants.count():   # noqa
            return Response({"error": "All Slots filed for this tournament"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Add the user to the tournament's participants
        tournament.participants.add(request.user.profile)
        serializer = TournamentSerializer(tournament)
        return Response(serializer.data, status=status.HTTP_200_OK)
