from django.contrib import admin
from django.conf.urls import patterns, include, url

from ellis_act.apps.housing_map import views

admin.autodiscover()

urlpatterns = patterns('',
    # Admin
    (r'^admin/', admin.site.urls),
    url(
        r'^$',
        views.NeighborhoodListView.as_view(),
        name='neighborhoods'
    ),
    url(
        r'^neighborhood/(?P<slug>[\w-]+)/$',
        views.NeighborhoodDetailView.as_view(),
        name='neighborhood'
    ),
    url(
        r'^stats/$',
        views.NeighborhoodStatView.as_view(),
        name='stats'
    ),
)
