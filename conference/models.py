from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=True)

class Book(models.Model):
    date = models.DateTimeField(null=True)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.CharField(max_length=125)

    class Meta:
        unique_together = ('date', 'room_id')