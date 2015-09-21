import os

from lib.utils import log

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping

from ellis_act.apps.housing_map.models import Neighborhood

class Command(BaseCommand):
    help = "Load sf neighborhood data into Address model"

    def handle(self, *args, **options):
        log('Loading neighborhood data ...\n', 'cyan')

        neighborhood_mapping = {
            'neighborhood' : 'neighborho',
            'geom' : 'POLYGON',
        }

        shps_dir = os.path.join(settings.BASE_DIR, 'data/shps')

        shp = os.path.join(shps_dir, 'sf-neighborhoods.shp')

        log('  Loading {} ...\n'.format(shp))

        lm = LayerMapping(
            Neighborhood,
            shp,
            neighborhood_mapping,
            encoding='utf-8'
        )

        lm.save(strict=True, verbose=True)

        log('    shp loaded and models created!\n', 'green')
