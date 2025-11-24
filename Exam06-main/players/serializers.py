from rest_framework import serializers
from .models import Player
from scores.models import Score

class PlayerSerializer(serializers.ModelSerializer):
    total_games = serializers.SerializerMethodField()
    wins = serializers.SerializerMethodField()
    draws = serializers.SerializerMethodField()
    losses = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['id', 'nickname', 'country', 'rating', 'total_games', 'wins', 'draws', 'losses', 'created_at']

    def get_total_games(self, obj):
        return obj.score_set.count()

    def get_wins(self, obj):
        return obj.score_set.filter(result='win').count()

    def get_draws(self, obj):
        return obj.score_set.filter(result='draw').count()

    def get_losses(self, obj):
        return obj.score_set.filter(result='loss').count()
