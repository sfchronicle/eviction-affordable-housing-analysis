import os

import csvkit
from lib.utils import log
from dateutil.parser import parse
from ipdb import set_trace as debugger

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from ellis_act.apps.housing_map.models import Eviction


class Command(BaseCommand):
    def handle(self, *args, **options):
        help = "Take model generated with "
        data = os.path.join(settings.BASE_DIR, 'data','2015-21-09-all-evictions-clean.csv')

        # model attributes
        datakeys = [
            'eviction_id', 'address', 'city', 'state', 'zipcode', 'file_date',
            'new_date', 'year', 'non_payment', 'breach', 'nuisance', 'illegal_use',
            'failure_to_sign_renewal', 'access_denial', 'unapproved_subtenant',
            'owner_move_in', 'demolition', 'capital_improvement',
            'substantial_rehab', 'ellis_act_withdrawal', 'condo_conversion',
            'roommate_same_unit', 'other_cause', 'late_payments',
            'lead_remediation', 'development', 'constraints',
            'constraints_date', 'supervisor_district', 'neighborhood',
            'latitude', 'longitude'
        ]

        str2bool = lambda x: str(x).lower() in ('TRUE', 'True', 'true')

        with open(data) as csvfile:
            reader = csvkit.reader(csvfile)
            headers = reader.next()
            count = 0

            log('LOADING RECORDS', 'cyan')

            for row in reader:
                eviction_dict = dict(zip(datakeys, row))
                try:
                    reason = [key for key, value in eviction_dict.iteritems() if str2bool(value)][0]

                except IndexError, e:
                    pass

                except UnicodeEncodeError, e:
                    debugger()

                try:
                    date = parse(eviction_dict['file_date'])
                except IndexError, e:
                    pass

                point = Point(
                    float(eviction_dict['longitude']),
                    float(eviction_dict['latitude'])
                )

                model_data = {
                    'eviction_id': eviction_dict['eviction_id'],
                    'address': eviction_dict['address'],
                    'city': eviction_dict['city'],
                    'state': eviction_dict['state'],
                    'zipcode': eviction_dict['zipcode'],
                    'file_date': date,
                    'new_date': eviction_dict['new_date'],
                    'year': eviction_dict['year'],
                    'eviction_reason': reason,
                    'constraints': eviction_dict['constraints'],
                    'constraints_date': eviction_dict['constraints_date'],
                    'supervisor_district': eviction_dict['supervisor_district'],
                    'neighborhood': eviction_dict['neighborhood'],
                    'geom': point
                }

                eviction = Eviction.objects.create(**model_data)
                count += 1

                log('  created <Eviction {}> [{}]'.format(eviction, count), 'green')

            log('{} eviction records created'.format(count))
