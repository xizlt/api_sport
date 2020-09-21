from django.contrib import admin
from order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    can_delete = False
    readonly_fields = ['product', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'paid', 'user']
    readonly_fields = ['id', 'created', 'updated', 'user']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    fields = (
        ('first_name', 'last_name', 'user'),
        'email',
        ('city', 'address', 'postal_code'),
        'note',
        'paid',
        ('created', 'updated')
    )
