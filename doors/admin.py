from django.contrib import admin
from .models import Door, Feature, FeatureCategory, Filter, FilterValue, Image


class ImageInline(admin.TabularInline):
    model = Image


class FeatureInline(admin.TabularInline):
    model = Feature
    prepopulated_fields = {'name_slug': ('name',), 'value_slug': ('value',)}


class DoorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'click_counter', 'in_stock')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ImageInline, FeatureInline]


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value')
    prepopulated_fields = {'name_slug': ('name',), 'value_slug': ('value',)}


class FeatureCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


class FilterValuesInline(admin.TabularInline):
    model = FilterValue
    prepopulated_fields = {'slug': ('name',)}


class FilterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [FilterValuesInline]


class FilterValuesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', "filter")
    prepopulated_fields = {'slug': ('name',)}


class ImageAdmin(admin.ModelAdmin):
    list_display = ('door', 'id', 'date_added', 'mimetype')


admin.site.register(Image, ImageAdmin)
admin.site.register(Door, DoorAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(FeatureCategory, FeatureCategoryAdmin)

admin.site.register(Filter, FilterAdmin)
admin.site.register(FilterValue, FilterValuesAdmin)
