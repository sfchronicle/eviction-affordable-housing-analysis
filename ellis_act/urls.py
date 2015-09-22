from django.contrib import admin
from django.conf.urls import patterns, include, url

from ellis_act.apps.housing_map.views import NeighborhoodDataListView

admin.autodiscover()

urlpatterns = patterns('',
    # Admin
    (r'^admin/', admin.site.urls),
    url(
        r'^$',
        NeighborhoodDataListView.as_view()
    ),
)
