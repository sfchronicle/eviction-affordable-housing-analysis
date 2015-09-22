from django.contrib import admin
from django.conf.urls import patterns, include, url

from ellis_act.apps.housing_map import views

admin.autodiscover()

urlpatterns = patterns('',
    # Admin
    (r'^admin/', admin.site.urls),
    url(
        r'^$',
        views.NeighborhoodDataListView.as_view()
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        views.NeighborhoodDetailView.as_view(),
        name='neighborhood'
    ),
)
