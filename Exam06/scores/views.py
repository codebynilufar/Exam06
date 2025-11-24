from rest_framework import viewsets
from .models import Score
from .serializers import ScoreSerializer

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        game_id = self.request.query_params.get('game_id')
        player_id = self.request.query_params.get('player_id')
        result = self.request.query_params.get('result')
        if game_id:
            qs = qs.filter(game_id=game_id)
        if player_id:
            qs = qs.filter(player_id=player_id)
        if result:
            qs = qs.filter(result=result)
        return qs
