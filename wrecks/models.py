from django.contrib.gis.db import models

class Wreck(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name
