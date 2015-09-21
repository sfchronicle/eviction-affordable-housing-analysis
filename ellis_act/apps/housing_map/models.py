from django.contrib.gis.db import models


class Neighborhood(models.Model):
    neighborhood = models.CharField(
        max_length=25,
        db_index=True
    )
    geom = models.MultiPolygonField(
        srid=4326
    )
    slug = models.SlugField(
        max_length=50,
        null=True
    )
    objects = models.GeoManager()

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('neighborhood', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        self.slug = slugify(self.neighborhood)
        super(Neighborhood, self).save(*args, **kwargs) # Call the "real" save() method.

    def __unicode__(self):
        return self.neighborhood


class Eviction(models.Model):
    EVICTION_REASON_CHOICES = (
        ('non_payment', 'non_payment'),
        ('breach', 'breach'),
        ('nuisance', 'nuisance'),
        ('illegal_use', 'illegal_use'),
        ('failure_to_sign_renewal', 'failure_to_sign_renewal'),
        ('access_denial', 'access_denial'),
        ('unapproved_subtenant', 'unapproved_subtenant'),
        ('owner_move_in', 'owner_move_in'),
        ('demolition', 'demolition'),
        ('capital_improvement', 'capital_improvement'),
        ('substantial_rehab', 'substantial_rehab'),
        ('ellis_act_withdrawal', 'ellis_act_withdrawal'),
        ('condo_conversion', 'condo_conversion'),
        ('roommate_same_unit', 'roommate_same_unit'),
        ('other_cause', 'other_cause'),
        ('late_payments', 'late_payments'),
        ('lead_remediation', 'lead_remediation'),
        ('development', 'development'),
    )

    CONSTRAINTS_CHOICES = (
        ('yes', 'yes'),
        (0, 'zero'),
        ('unknown', 'unknown')
    )

    neighborhood =  models.ForeignKey(Neighborhood, null=True)

    eviction_id = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, )  # zip
    file_date = models.DateField()
    new_date = models.CharField(max_length=255)
    year = models.CharField(max_length=255)

    eviction_reason = models.CharField(
        max_length=255, choices=EVICTION_REASON_CHOICES)

    constraints = models.CharField(
        max_length=255, choices=CONSTRAINTS_CHOICES, default='unknown')

    constraints_date = models.CharField(max_length=255, blank=True, null=True)
    supervisor_district = models.CharField(max_length=2, blank=True, null=True)
    raw_neighborhood = models.CharField(max_length=255, blank=True, null=True)

    geom = models.PointField(srid=4326)
    objects = models.GeoManager()


    def __unicode__(self):
        return self.address
