import uuid

from django.db import models


class Description(models.Model):
    DIFFICULTY_CHOICES = {
        1: 'Very Easy',
        2: 'Easy',
        3: 'Normal',
        4: 'Hard',
        5: 'Very Hard'
    }

    description_text = models.TextField(blank=True, null=True)
    n_players = models.TextField('number of players')
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
    cover_photo = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class BookedDate(models.Model):
    date = models.DateField()

    def __str__(self):
        return self.date.strftime('%a, %d %b %Y')


class GameItem(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    booked_dates = models.ManyToManyField(BookedDate)

    def add_booked_date(self, date):
        booked_date, created = BookedDate.objects.get_or_create(date=date)
        self.booked_dates.add(booked_date)

    def remove_booked_date(self, date):
        try:
            booked_date = BookedDate.objects.get(date=date)
            self.booked_dates.remove(booked_date)
        except BookedDate.DoesNotExist:
            pass
