from django.contrib import admin

from .models import CarMake, CarModel
# from .models import related models


# Register your models here.

# CarModelInline class
class CarModelInLine(admin.StackedInline):
    model =CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields=['year','make','name','type','dealer_id' ]
    list_filter=['year']
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines =[CarModelInLine]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)