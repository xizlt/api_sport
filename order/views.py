from urllib import request

from django.contrib.auth.models import User
from django.db.models import Sum, DecimalField, F
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from order.models import Order, OrderItem
from order.permissions import OrderPermission
from order.serializers import OrderSerializer, ItemOrderSerializer


class OrderView(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (OrderPermission,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        elif not self.request.user.is_authenticated:
            pass
        else:
            return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.validated_data['user'] = self.request.user
        serializer.save()


class ItemView(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = ItemOrderSerializer
    permission_classes = (IsAdminUser,)

    # def get_queryset(self):
    #     if self.queryset.filter(order__user=self.request.user).exists():
    #         return self.queryset.filter(order__user=self.request.user)
    #     return self.queryset
