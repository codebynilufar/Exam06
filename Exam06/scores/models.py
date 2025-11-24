from django.db import models
from games.models import Game
from players.models import Player

RESULT_CHOICES = (
    ('win', 'Win'),
    ('draw', 'Draw'),
    ('loss', 'Loss'),
)

POINTS_MAP = {
    'win': 10,
    'draw': 5,
    'loss': 0,
}

class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    points = models.IntegerField()
    opponent_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.points = POINTS_MAP[self.result]
        super().save(*args, **kwargs)
        self.update_player_rating()

    def update_player_rating(self):
        scores = Score.objects.filter(player=self.player)
        self.player.rating = sum([s.points for s in scores])
        self.player.save()

    class Meta:
        ordering = ['-created_at']
