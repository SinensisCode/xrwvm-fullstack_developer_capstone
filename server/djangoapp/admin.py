from django.contrib import admin
from .models import CarMake, CarModel

# CarModelInline class
class CarModelInline(admin.ModelAdmin):
    fields = ('name', 'description')
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ('name')
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

# Register your models here.
admin.site.register(CarModel)
admin.site.register(CarMake)