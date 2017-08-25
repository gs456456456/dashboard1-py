from django.contrib import admin

# Register your models here.
from django.contrib import admin
from app1 import models

class PostAdmin(admin.ModelAdmin):
    list_display=('sunmax','sunmin','now')
    # ordering=()

class TempAdmin(admin.ModelAdmin):
    list_display = ('temperaturemax','temperaturemin','now')

class WaterAdmin(admin.ModelAdmin):
    list_display = ('waterpressuremax','waterpressuremin','now')

admin.site.register(models.configsun,PostAdmin)
admin.site.register(models.configtemp,TempAdmin)
admin.site.register(models.configwater,WaterAdmin)
