from django.contrib import admin

from .models import Car


class CarAdmin(admin.ModelAdmin):
    list_display = ['car', 'model', 'color', 'pub_date', 'customer', 'license_plate']


admin.site.register(Car, CarAdmin)
