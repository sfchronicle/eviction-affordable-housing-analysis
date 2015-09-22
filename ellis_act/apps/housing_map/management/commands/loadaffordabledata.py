import os

import csvkit
from lib.utils import log
from dateutil.parser import parse
from ipdb import set_trace as debugger

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from loaddataset import get_neighborhood
from ellis_act.apps.housing_map.models import AffordableHousing, Neighborhood


class Command(BaseCommand):
    def handle(self, *args, **options):
        help = "Load AffordableHousing model"
        data = os.path.join(settings.BASE_DIR, 'data','2015-21-09-affordable-housing.csv')

        # model attributes
        datakeys = [
            'action_date','year','app_id','address','zipcode',
            'latitude','longitude','accuracy_score','description','prop_use',
            'block','lot','blocklot','units','netunits','total_project_units',
            'fm','ext_use','action','staff','aff_target','raw_neighborhood',
            'supervisor_district','yr_qtr','city','state','county'
        ]

        with open(data) as csvfile:
            reader = csvkit.reader(csvfile)
            headers = reader.next()
            count = 0

            log('LOADING AFFORDABLE HOUSING RECORDS', 'cyan')

            for row in reader:
                affordablehousing_dict = dict(zip(datakeys, row))


                try:
                    date = parse(affordablehousing_dict['action_date'])
                except IndexError, e:
                    log('  date parsing error {}'.format(e), 'red')

                point = Point(
                    float(affordablehousing_dict['longitude']),
                    float(affordablehousing_dict['latitude'])
                )

                neighborhood = get_neighborhood(point)

                try:
                    neighborhood_id = neighborhood.id
                except AttributeError, e:
                    neighborhood_id = None

                model_data = {
                    'neighborhood_id': neighborhood_id,
                    'action_date': date,
                    'year': affordablehousing_dict['year'],
                    'app_id': affordablehousing_dict['app_id'],
                    'address': affordablehousing_dict['address'],
                    'zipcode': affordablehousing_dict['zipcode'],
                    'accuracy_score': affordablehousing_dict['accuracy_score'],
                    'description': affordablehousing_dict['description'],
                    'prop_use': affordablehousing_dict['prop_use'],
                    'block': affordablehousing_dict['block'],
                    'lot': affordablehousing_dict['lot'],
                    'blocklot': affordablehousing_dict['blocklot'],
                    'units': affordablehousing_dict['units'],
                    'netunits': affordablehousing_dict['netunits'],
                    'total_project_units': affordablehousing_dict['total_project_units'],
                    'fm': affordablehousing_dict['fm'],
                    'ext_use': affordablehousing_dict['ext_use'],
                    'action': affordablehousing_dict['action'],
                    'staff': affordablehousing_dict['staff'],
                    'aff_target': affordablehousing_dict['aff_target'],
                    'raw_neighborhood': affordablehousing_dict['raw_neighborhood'],
                    'supervisor_district': affordablehousing_dict['supervisor_district'],
                    'yr_qtr': affordablehousing_dict['yr_qtr'],
                    'city': affordablehousing_dict['city'],
                    'state': affordablehousing_dict['state'],
                    'county': affordablehousing_dict['county'],
                    'geom': point
                }

                affordablehousing = AffordableHousing.objects.create(**model_data)
                count += 1

                log('  created <AffordableHousing {}> [{}]'.format(affordablehousing, count), 'green')

            log('{} affordable housing records created'.format(count))
