from django.db import models


class Store(models.Model):
    address = models.CharField(db_index=True, max_length=100, unique=True)
    open_hours = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11)
    manager = models.CharField(max_length=20)

    def __str__(self):
        return self.address
