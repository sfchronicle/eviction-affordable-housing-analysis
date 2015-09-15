from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class BaseEviction(models.Model):
    """Base Eviction Model class"""
    eviction_id = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    file_date = models.DateField(blank=True, null=True)
    new_file_date = models.DateTimeField(blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    client_location = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return '{} ({})'.format(self.address, self.year)

    class Meta:
        abstract = True


class EllisAct(BaseEviction):
    ellis_act_withdrawl = models.CharField(
        max_length=255, blank=True, null=True)

    neighborhood = models.CharField(
        max_length=255, blank=True, null=True)


class OwnerMoveIn(BaseEviction):
    did_owner_movein = models.CharField(max_length=255, blank=True, null=True)
    constraints = models.CharField(max_length=255)
    constraints_date = models.CharField(max_length=255, blank=True, null=True)
    supervisor_district = models.IntegerField(blank=True, null=True)
    neighborhood = models.CharField(max_length=255, blank=True, null=True)
