from rest_framework import serializers
from .models import Score
from games.serializers import GameSerializer
from players.serializers import PlayerSerializer

class ScoreSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)
    player = PlayerSerializer(read_only=True)
    game_id = serializers.IntegerField(write_only=True)
    player_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Score
        fields = ['id', 'game', 'player', 'result', 'points', 'opponent_name', 'created_at', 'game_id', 'player_id']

    def create(self, validated_data):
        game_id = validated_data.pop('game_id')
        player_id = validated_data.pop('player_id')
        score = Score.objects.create(game_id=game_id, player_id=player_id, **validated_data)
        return score
