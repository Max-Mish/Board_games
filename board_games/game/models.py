from django.db import models


class Description(models.Model):
    description_text = models.TextField()
    n_players = models.IntegerField()
    duration = models.IntegerField()
    difficulty = models.CharField(max_length=20)

    def __str__(self):
        return self.description_text


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Game(models.Model):
    name = models.CharField(max_length=50)
    description = models.ForeignKey(Description, on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ManyToManyField(Category)
    publisher = models.CharField(max_length=50)
    cost = models.IntegerField()

    def __str__(self):
        return self.name
