from django.db import models
from django.core.exceptions import ValidationError

class Player(models.Model):
    nickname = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=50)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname

    def delete(self, *args, **kwargs):
        if self.score_set.exists():
            raise ValidationError(f"Cannot delete player with game history. Player has {self.score_set.count()} recorded games.")
        return super().delete(*args, **kwargs)
