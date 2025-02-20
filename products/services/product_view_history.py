from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.models import ProductViewHistory
from products.serializers import ProductViewHistorySerilizer
from drf_yasg.utils import swagger_auto_schema

class ProductViewHistoryCreate(APIView):
    serializers_class = ProductViewHistorySerilizer
    @swagger_auto_schema(request_body=ProductViewHistorySerilizer)
    def post(self,request):
        serializer = ProductViewHistorySerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



