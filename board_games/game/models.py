from django.db import models

# from .managers import GameManager


class Description(models.Model):
    DIFFICULTY_CHOICES = {
        1: 'Very Easy',
        2: 'Easy',
        3: 'Normal',
        4: 'Hard',
        5: 'Very Hard'
    }

    description_text = models.TextField(blank=True, null=True)
    n_players = models.IntegerField('number of players')
    duration = models.IntegerField()
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return self.description_text


class Category(models.Model):
    name = models.CharField(db_index=True, max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Game(models.Model):
    name = models.CharField(db_index=True, max_length=50, unique=True)
    description = models.ForeignKey(Description, on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ManyToManyField(Category)
    publisher = models.CharField(max_length=50)
    cost = models.IntegerField()


    def __str__(self):
        return self.name
