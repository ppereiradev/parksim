from django.contrib.gis.db.models import PointField
from django.db import models


class Marker(models.Model):

    name = models.CharField(max_length=255)
    location = PointField()
    camera = models.CharField(max_length=255)
    parkspace = models.IntegerField()


    def __str__(self):
        return self.name