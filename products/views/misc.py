from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from products.models import Order, Review, Category
from products.permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly
from products.serializers import OrderSerializers, ReviewSerilizer, CategorySerilizer

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

class ReviewVievSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerilizer




class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerilizer

