from django.contrib import admin
from .models import Eviction, Neighborhood

@admin.register(Eviction)
class EvictionAdmin(admin.ModelAdmin):
    date_hierachy = 'file_date'
    readonly_fields = ('eviction_id', 'address',
        'zipcode', 'file_date', 'eviction_reason', 'supervisor_district',)
    list_filter = ('neighborhood', 'file_date', 'zipcode', 'eviction_reason')
    list_display = ('eviction_id', 'address', 'zipcode',
        'neighborhood', 'file_date', 'eviction_reason', 'supervisor_district',)
