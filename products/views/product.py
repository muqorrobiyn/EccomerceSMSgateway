from django.db import models
from django_filters import rest_framework as django_filters
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from products.filters import ProductFilter
from products.models import Product
from products.permissions import IsStaffOrReadOnly
from products.serializers import ProductSerilizer
from rest_framework.decorators import action

class CustomPagination(PageNumberPagination):
    page_size = 3

class ProductViewset(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerilizer
    pagination_class = CustomPagination
    filter_backends =(django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['name','description']

    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)
        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_products = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5]
        related_serializers = ProductSerilizer(related_products, many=True )
        return Response({
            'product': serializer.data,
            'related_products': related_serializers.data
        })
    @action(detail=False,methods=['get'])
    def top_rated(self,request):
        # Assuming a related name of "reviews" from Review model to Product model
        top_products = Product.objects.annotate(avg_rating=models.Avg('reviews_rating')).order_by('-avg_rating')[:2]
        serializer = ProductSerilizer(top_products,many=True)
        return Response(serializer.data)


    @action(detail=False,methods=['get'])
    def average_rating(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()

        if reviews.count() == 0:
            return Response({'average_rating': 'No reviews yet!'})

        avg_rating = sum([review.rating for review in reviews]) / reviews.count()
        return Response({'average_rating': avg_rating})
