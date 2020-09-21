from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from shop.models import Product, Category, Brand
from shop.serializers import ProductSerializer, CategorySerializer, BrandSerializer
from shop.service import ProductFilter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


class ProductView(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.filter(available=True).select_related('category', 'brand').prefetch_related(
        'description', 'specification')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name']
    # ordering_fields = ['price', 'brand', 'rating', 'name']


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
