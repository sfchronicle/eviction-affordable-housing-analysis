from datetime import date

from django.db.models import Sum, Count, Prefetch, Avg
from bakery.views import BuildableTemplateView

from ellis_act.apps.housing_map.models import Eviction, AffordableHousing, Neighborhood

class NeighborhoodDataListView(BuildableTemplateView):
    template_name = 'data_list.html'

    def get_context_data(self, **kwargs):
        context = super(NeighborhoodDataListView, self).get_context_data(**kwargs)
        context['neighborhoods'] = Neighborhood.objects\
            .prefetch_related(
                Prefetch(
                    'eviction_set',
                    queryset=Eviction.objects.filter(file_date__gte=date(2005, 1, 1))
                ),
                'affordablehousing_set'
            ).all()
        return context


class NeighborhoodDetailView(BuildableTemplateView):
    template_name = 'neighborhood_detail.html'

    def get_context_data(self, **kwargs):
        context = super(NeighborhoodDetailView, self).get_context_data(**kwargs)
        context['neighborhood'] = Neighborhood.objects\
            .prefetch_related(
                Prefetch(
                    'eviction_set',
                    queryset=Eviction.objects.filter(file_date__gte=date(2005, 1, 1))
                ),
                'affordablehousing_set'
            ).get(**kwargs)
        return context
