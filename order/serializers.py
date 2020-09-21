from django.db.models import Sum, F, DecimalField
from rest_framework import serializers, response
from rest_framework.fields import IntegerField, FloatField, CharField
from rest_framework.response import Response
from rest_framework.utils import model_meta

from .models import Order, OrderItem


class ItemOrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    id = serializers.IntegerField(source='pk', default=None)

    # product = serializers.HyperlinkedRelatedField(read_only=True, view_name='product-detail')
    # product = ProductShotSerializer()

    class Meta:
        model = OrderItem
        fields = ['total_price', 'price', 'quantity', 'product', 'id', 'order']

    @staticmethod
    def get_total_price(obj):
        return OrderItem.get_cost(obj)


class OrderSerializer(serializers.ModelSerializer):
    goods = ItemOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'phone', 'note', 'goods']

    def create(self, validated_data):
        items = validated_data.pop('goods', [])
        order = Order.objects.create(**validated_data)
        for item in items:
            OrderItem.objects.create(order=order, **item)
        return order

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.address = validated_data['address']
        instance.city = validated_data['city']
        instance.email = validated_data['email']
        instance.postal_code = validated_data['postal_code']
        instance.phone = validated_data['phone']
        instance.note = validated_data['note']
        instance.save()
        item_in_order = set(OrderItem.objects.filter(order=instance).values_list('id', flat=True))
        item_in_form = set()
        for item in validated_data['goods']:

            item_in_form.add(item['pk'])
            if not item['pk']:
                OrderItem.objects.create(quantity=item['quantity'],
                                         price=item['price'],
                                         product=item['product'],
                                         order=item['order'])
            OrderItem.objects.filter(id=item['pk']).update(quantity=item['quantity'],
                                                           price=item['price'],
                                                           product=item['product'],
                                                           order=item['order'])
        OrderItem.objects.filter(id__in=item_in_order.difference(item_in_form)).delete()

        return instance
