from rest_framework import serializers

from .models import Product, Description, Specification, Category, Brand


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ['name', 'benefit']


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['name', 'benefit']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    description = DescriptionSerializer(many=True, read_only=True)
    specification = SpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ['updated', 'created', 'available']


class ProductShotSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField()
    # brand = serializers.StringRelatedField()
    product_id = serializers.IntegerField(source='pk', default=None)

    class Meta:
        model = Product
        fields = ["product_id", "name", "image",  "rating", 'id']
        # exclude = ['updated', 'created', 'available', 'specification', 'description', 'link', 'category', 'brand']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']
