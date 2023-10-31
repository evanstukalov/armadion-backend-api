from django.contrib import admin
from .models import Door, Feature, FeatureCategory


class DoorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'click_counter', 'in_stock')
    prepopulated_fields = {'slug': ('title',)}


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value', 'feature_category')


class FeatureCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'door')


admin.site.register(Door, DoorAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(FeatureCategory, FeatureCategoryAdmin)
