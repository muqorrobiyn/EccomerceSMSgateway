# from rest_framework import views,status
# from rest_framework.response import Response
# import stripe
# from django.conf import settings
# from .models import Payment
# from products.models import Order
#
# stripe.api_key = settings.STRIPE_SECRET_KEY
#
# class CreateChargeViews(views.APIView):
#     def post(self,request, *args,**kwargs):
#         stripe_token = request.data.get('stripe_token')
#         order_id = request.data.get('order_id')
#
#         try:
#             order = Order.objects.get(id=order_id)
#
#         except Order.DoesNotExist:
#             return Response({'error':'Order not found'}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             total_amount = order.product.price * order.quantity
#             charge = stripe.Charge.create(
#                 amount=int(total_amount*100),
#                 currency='usd',
#                 source=stripe_token,
#             )
#             Payment.objects.create(
#                 order=order,
#                 stripe_charge_id=charge['id'],
#                 amount=total_amount
#             )
#
#             order.is_paid = True
#             order.save()
#             return Response({'status':'Payment successfully'}, status=status.HTTP_200_OK)
#
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import views, status
from rest_framework.response import Response
import stripe
from django.conf import settings
from .models import Payment
from products.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateChargeViews(views.APIView):
    def post(self, request, *args, **kwargs):
        stripe_token = request.data.get('stripe_token')
        order_id = request.data.get('order_id')

        if not stripe_token:
            return Response({'error': 'Stripe token required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            total_amount = order.product.price * order.quantity  # Mahsulot narxi * miqdor
            if total_amount <= 0:
                return Response({'error': 'Invalid total amount'}, status=status.HTTP_400_BAD_REQUEST)

            charge = stripe.Charge.create(
                amount=int(total_amount * 100),  # Sentlarga o‘girish
                currency='usd',
                source=stripe_token,  # `sourse` emas, `source`
            )

            Payment.objects.create(
                order=order,
                stripe_charge_id=charge['id'],
                amount=total_amount
            )

            order.is_paid = True
            order.save()
            return Response({'status': 'Payment successfully'}, status=status.HTTP_200_OK)

        except stripe.error.CardError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            return Response({'error': 'Payment processing error'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
