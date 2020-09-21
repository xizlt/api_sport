import datetime

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Category, Description, Specification, Brand


def pars_update(modeladmin, request, queryset):
    from parse_.parsing import parse
    for obj in queryset:
        parse(obj.url, obj.name)
        # Category.objects.filter(name=obj.name, url=obj.url).update(updated=datetime.datetime.today())


pars_update.short_description = 'Update products'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'url',)
    list_display = ('name', 'url',)
    actions = [pars_update]
    list_editable = ('url',)


@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    fields = ('name', 'benefit',)
    list_display = ('name', 'benefit',)


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    fields = ('name', 'benefit',)
    list_display = ('name', 'benefit',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = (
        'name', 'brand', 'category', 'image', 'price', 'old_price', 'available', 'created', 'updated', 'specification',
        'description')
    readonly_fields = ('created', 'updated',)
    list_display = ('name', 'category', 'get_image', 'price', 'old_price', 'available',)
    list_editable = ('old_price', 'available',)
    list_filter = ('created', 'category', 'brand')
    save_on_top = True

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image}" width="75">')
        else:
            return '-'

    get_image.short_description = 'photo'
