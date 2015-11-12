from datetime import date

from django.db import connection
from django.db.models import Sum, Count, Prefetch, Avg
from bakery.views import BuildableTemplateView

from ellis_act.apps.housing_map.models import Eviction, AffordableHousing, Neighborhood

class NeighborhoodListView(BuildableTemplateView):
    template_name = 'neighborhood_list.html'

    def get_context_data(self, **kwargs):
        context = super(NeighborhoodListView, self).get_context_data(**kwargs)
        context['neighborhoods'] = Neighborhood.objects\
            .prefetch_related(
                Prefetch(
                    'eviction_set',
                    queryset=Eviction.objects.filter(file_date__gte=date(2005, 1, 1))\
                    .exclude(eviction_reason=['lead_remediation', 'capital_improvement'])
                ),
                'affordablehousing_set'
            ).exclude(neighborhood='Golden Gate Park')
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


class NeighborhoodStatView(BuildableTemplateView):
    template_name = 'stats.html'

    def get_context_data(self, **kwargs):
        context = super(NeighborhoodStatView, self).get_context_data(**kwargs)
        """
        TOTAL number of evictions by NEIGHBORHOOD
        """
        context['neighborhoods'] = Neighborhood.objects\
            .filter(eviction__file_date__gte=date(2005, 1, 1))\
            .annotate(num_evictions=Count('eviction'))\
            .order_by('-num_evictions')

        """
        Evictions by YEAR
        """
        truncate_date = connection.ops.date_trunc_sql('year', 'file_date')
        context['evictions_by_year'] = Eviction.objects\
            .filter(file_date__gte=date(2005, 1, 1))\
            .extra({'year': truncate_date})\
            .values('year').annotate(Count('pk')).order_by('year')

        """
        TOTAL EVICTIONS
        """
        context['total_evictions'] = Eviction\
            .objects.filter(file_date__gte=date(2005, 1, 1), neighborhood__isnull=False).count()

        """
        Total Evictions by reason
        """
        context['total_evictions_by_reason'] = Eviction.objects\
            .filter(file_date__gte=date(2005, 1, 1))\
            .values('eviction_reason')\
            .annotate(Count('pk')).order_by('-pk__count')

        return context
