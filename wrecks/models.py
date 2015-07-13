from django.contrib.gis.db import models

SOURCE_CHOICES = (
    (0, 'NOAA Automated Wrecks and Obstructions Information System (AWOIS)'),
    (1, 'NOAA Electronic Navigational Charts (ENC)'),
)

class WreckType(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

class Wreck(models.Model):
    name = models.CharField(max_length=255, blank=True)
    history = models.TextField(blank=True)
    wreck_type = models.ForeignKey('WreckType')
    year_sunk = models.SmallIntegerField(blank=True, null=True)
    source = models.SmallIntegerField(choices=SOURCE_CHOICES)
    source_identifier = models.IntegerField(blank=True, null=True)
    depth_meters = models.FloatField(blank=True, null=True)
    location = models.PointField()

    objects = models.GeoManager()

    class Meta:
        managed = True

    def __unicode__(self):
        return self.name
