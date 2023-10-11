from django.contrib import admin
from .models import Door, Series, DoorType

admin.site.register(Door)
admin.site.register(Series)
admin.site.register(DoorType)