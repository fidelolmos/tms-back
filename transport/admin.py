from django.contrib import admin
from .models import Direction, Order, Route, TMS

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'street', 'city', 'state', 'zip_code', 'country', 'lat', 'lon')
    search_fields = ('name', 'street', 'city', 'state', 'zip_code', 'country')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'created_by', 'origin', 'destination', 'delivery_address')
    search_fields = ('name', 'created_by__email', 'origin__name', 'destination__name')
    list_filter = ('date',)

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'origin', 'destination', 'distance')
    search_fields = ('name', 'origin__name', 'destination__name')

@admin.register(TMS)
class TMSAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle', 'driver', 'single_route', 'start_date', 'end_date', 'total_distance')
    search_fields = ('name', 'vehicle', 'driver__email')
    list_filter = ('single_route', 'start_date', 'end_date')
