from django.contrib import admin
from .models import Door, Characteristic, CategoryCharacteristic

class DoorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'click_counter', 'in_stock')
    prepopulated_fields = {'slug': ('title',)}

class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value')

class CategoryCharacteristicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Door, DoorAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(CategoryCharacteristic, CategoryCharacteristicAdmin)

