from django.contrib import admin

# Register your models here.

from .models import my_user, Ride, vehicle

admin.site.register(my_user)
admin.site.register(Ride)
admin.site.register(vehicle)
