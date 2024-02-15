from datetime import timedelta, date

from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models import CustomUser
from game.models import Game
from poll.models import Choice


class Booking(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    opening_date = models.DateField(auto_now_add=True)
    closing_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(default=date.today() + timedelta(weeks=1))

    def __str__(self):
        return f'{self.user} | {self.game}'

    class Meta:
        permissions = [
            (
                "view_filtered_booking",
                "Can view filtered booking"
            ),
        ]


class Vote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} | {self.choice}'


@receiver(post_save, sender=Vote)
def my_callback(sender, instance, created, **kwargs):
    if created:
        vote = instance
        choice_id = vote.choice_id
        choice = Choice.objects.get(pk=choice_id)
        choice.n_votes = F('n_votes') + 1
        choice.save()
