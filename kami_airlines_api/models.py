from django.db import models

class Airplane(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    passenger_count = models.PositiveIntegerField()

    def __str__(self):
        return f"Airplane {self.id}"