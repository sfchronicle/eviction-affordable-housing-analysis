import os

from postgres_copy import CopyMapping

from django.conf import settings
from django.core.management.base import BaseCommand

from ellis_act.apps.housing_map.models import EllisAct, OwnerMoveIn


class Command(BaseCommand):
    def handle(self, *args, **options):
        help = "Load database with CSV"
        ellis_act_csv = os.path.join(
            settings.BASE_DIR, 'data', 'ellis_act_notices_refined.csv')

        owner_evictions_csv = os.path.join(
            settings.BASE_DIR, 'data', 'owner_movein_refined.csv')

        base_dict = dict(
            eviction_id='eviction_id',
            address='address',
            city='city',
            state='state',
            zipcode='zip',
            file_date='file_date',
            new_file_date='new_file_date',
            year='year',
            client_location='client_location',
            latitude='lat',
            longitude='long',
        )

        ellis_act_dict = base_dict
        ellis_act_dict['neighborhood'] = 'neighborhood'
        ellis_act_dict['ellis_act_withdrawl'] = 'ellis_act_withdrawl'

        owner_evictions_dict = base_dict
        owner_evictions_dict['did_owner_movein'] = 'owner_movein'
        owner_evictions_dict['constraints'] = 'constraints'
        owner_evictions_dict['constraints_date'] = 'constraints_date'
        owner_evictions_dict['supervisor_district'] = 'supervisor_district'
        owner_evictions_dict['neighborhood'] = 'neighborhood'

        load_ellis_act = CopyMapping(
            EllisAct, ellis_act_csv, ellis_act_dict)

        load_owner_evictions = CopyMapping(
            OwnerMoveIn, owner_evictions_csv, owner_evictions_dict)

        load_ellis_act.save()
        load_owner_evictions.save()
