from django.contrib import admin
from .models import Eviction, Neighborhood, AffordableHousing

@admin.register(Eviction)
class EvictionAdmin(admin.ModelAdmin):
    date_hierachy = 'file_date'
    readonly_fields = ('eviction_id', 'address',
        'zipcode', 'file_date', 'eviction_reason', 'supervisor_district',)
    list_filter = ('neighborhood', 'year', 'eviction_reason',)
    list_display = ('eviction_id', 'address', 'neighborhood',
        'file_date', 'year','eviction_reason', 'supervisor_district',)


@admin.register(AffordableHousing)
class AffordableHousingAdmin(admin.ModelAdmin):
    date_hierachy = 'action_date'
    list_filter = ('neighborhood', 'year',)
    list_display = ('app_id', 'address', 'neighborhood',
        'action_date', 'year', 'total_project_units')
