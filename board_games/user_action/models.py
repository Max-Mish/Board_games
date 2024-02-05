from django.db import models

from user.models import User
from game.models import Game
from poll.models import Choice


class Booking(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    return_period = models.DateField()
    opening_date = models.DateField()
    closing_date = models.DateField(null=True)

    def __str__(self):
        return f'{self.user} | {self.game}'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} | {self.choice}'
