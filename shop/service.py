import django_filters.rest_framework as filter

from shop.models import Product


class CharFilterInFilter(filter.BaseInFilter, filter.CharFilter):
    pass


class ProductFilter(filter.FilterSet):
    name = CharFilterInFilter(field_name='name')
    brand = CharFilterInFilter(field_name='brand__name')
    price = filter.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('rating', 'rating'),
        ),
    )

    class Meta:
        model = Product
        fields = ['name', 'brand']
