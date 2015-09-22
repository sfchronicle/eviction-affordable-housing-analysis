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

    neighborhood =  models.ForeignKey(Neighborhood, null=True, db_index=True)

    eviction_id = models.CharField(max_length=255, null=True, db_index=True)
    address = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    city = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    state = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    zipcode = models.CharField(max_length=255, db_index=True)  # zip
    file_date = models.DateField(db_index=True)
    new_date = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    year = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    eviction_reason = models.CharField(
        max_length=255, choices=EVICTION_REASON_CHOICES)

    constraints = models.CharField(
        max_length=255, choices=CONSTRAINTS_CHOICES, default='unknown')

    constraints_date = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    supervisor_district = models.CharField(max_length=2, blank=True, null=True, db_index=True)
    raw_neighborhood = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    geom = models.PointField(srid=4326)
    objects = models.GeoManager()


    def __unicode__(self):
        return self.address


class AffordableHousing(models.Model):
    neighborhood =  models.ForeignKey(Neighborhood, null=True, db_index=True)
    action_date = models.DateField(help_text='When project was completed', db_index=True)  # actdt
    year = models.CharField(max_length=4, help_text='Year project was completed')

    app_id = models.CharField(
        max_length=255, blank=True, null=True, help_text='Application number', db_index=True)

    address = models.CharField(max_length=255, blank=True, null=True, db_index=True)  # full address
    zipcode = models.CharField(max_length=255, blank=True, null=True, db_index=True)  # zip

    accuracy_score = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    description = models.TextField(blank=True, null=True, db_index=True)  # descript

    prop_use = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    block = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    lot = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    blocklot = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    units = models.IntegerField(help_text='Gross units', db_index=True)

    netunits = models.CharField(max_length=255,
        help_text='Net Units (so for example, a project \
        with 40 units is built over an existing 10 unit building, \
        then the net addition to the housing stock is 30 net units)',
        db_index=True
    )

    total_project_units = models.IntegerField(
        help_text='number of affordable housing units in project', db_index=True
    )  # aff_hsg

    fm = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    ext_use = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    action = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    staff = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    aff_target = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    raw_neighborhood = models.CharField(max_length=255, blank=True, null=True, db_index=True)  # district_1
    supervisor_district = models.CharField(max_length=2, blank=True, null=True, db_index=True)  # supervis_1

    yr_qtr = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    city = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    state = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    county = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    geom = models.PointField(srid=4326)
    objects = models.GeoManager()

    class Meta:
        verbose_name_plural = 'Affordable housing'

    def __unicode__(self):
        return self.address
