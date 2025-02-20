from django.db import models
from rest_framework import serializers
from products.models import Product, Review, Category, ProductViewHistory

class ProductSerilizer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True,required=False)
    class Meta:
        model = Product
        fields = ['id','name','description', 'price', 'stock', 'avg_rating']


class ReviewSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class CategorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductViewHistorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = ProductViewHistory
        fields = '__all__'