from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
import random
import requests
import logging
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import viewsets,status
import uuid
from .serializers import SMSSerializer, VerifySMSSerializer
from django.conf import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# logging.basicConfig(level=logging.INFO)
User = get_user_model()
SMS_KEY = settings.SMS_KEY


class SMSLoginViewSet(viewsets.ViewSet):

       #sms yuborish
    # @action(detail=False, methods=['post'])
    # def send_sms(self,request):
    #     serializer = SMSSerializer(data=request.data)
    #     if serializer.is_valid():
    #         phone_number = serializer.validated_data['phone_number']
    #         # 6 honali randomli verificatsiya kodini generasiya qilish
    #         verification_code = str(random.randint(100000, 999999))
    #         #send SMS via infobip
    #         url = 'https://3835jj.api.infobip.com/sms/2/text/advanced'
    #         headers = {
    #             'Authorization': SMS_KEY,
    #             'Content-Type': 'application/json',
    #             'Accept': 'application/json'
    #         }
    #
    #         payload = {
    #             'messages': [
    #                 {
    #                     'from':'EcommerceAPi',
    #                     'destinations': [
    #                         {
    #                             'to': phone_number
    #                         }
    #                     ],
    #                     'text': f'Your verifications code is {verification_code}'
    #                 }
    #             ]
    #         }
    #         response = requests.post(url,json=payload,headers=headers)
    #         logger.info(f"Infobip API response: {response.status_code}, {response.text}")
    #         if response.status_code == 200:
    #             # Store the verification code and phone number in cache 5 minutes
    #             cache.set(phone_number,verification_code, 300)
    #             logger.info(f"Cache set: {phone_number} -> {verification_code}")
    #             return Response({'message': 'SMS sent successfully'}, status=status.HTTP_200_OK)
    #         return Response({'message': 'Failed to send SMS'}, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


     #whatsappdan habar yuborish
       @action(detail=False, methods=['post'])
       def send_sms(self, request):
           serializer = SMSSerializer(data=request.data)
           if serializer.is_valid():
               phone_number = serializer.validated_data['phone_number']
               verification_code = str(random.randint(100000, 999999))  # 6 xonali tasdiqlash kodi

               # Infobip WhatsApp API URL
               url = 'https://3835jj.api.infobip.com/whatsapp/1/message/template'
               headers = {
                   'Authorization': SMS_KEY,  # API kalitingizni tekshiring
                   'Content-Type': 'application/json',
                   'Accept': 'application/json'
               }

               payload = {
                   "messages": [
                       {
                           "from": "447860099299",  # Infobip'dagi WhatsApp raqamingiz
                           "to": phone_number,
                           "messageId": str(uuid.uuid4()),  # Unikal xabar ID
                           "content": {
                               "templateName": "verification_template",  # WhatsApp'dagi shablon nomi
                               "templateData": {
                                   "body": {
                                       "placeholders": [verification_code]  # Kodni shablonda almashtiramiz
                                   }
                               },
                               "language": "en"  # Shablon tili
                           }
                       }
                   ]
               }

               response = requests.post(url, json=payload, headers=headers)
               logger.info(f"Infobip API response: {response.status_code}, {response.text}")

               if response.status_code == 200 or response.status_code == 201:
                   # 5 daqiqaga cache'ga saqlash
                   cache.set(phone_number, verification_code, 300)
                   logger.info(f"Cache set: {phone_number} -> {verification_code}")
                   return Response({'message': 'WhatsApp message sent successfully'}, status=status.HTTP_200_OK)

               return Response({'message': 'Failed to send WhatsApp message'}, status=status.HTTP_400_BAD_REQUEST)

           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       @action(detail=False, methods=['post'])
       def verify_sms(self, request):
            logger.info(f"Received verify_sms data: {request.data}")  # Logga chiqarish

            serializer = VerifySMSSerializer(data=request.data)
            if serializer.is_valid():
                phone_number = serializer.validated_data['phone_number']
                verification_code = serializer.validated_data['verification_code']

                cache_code = cache.get(phone_number)  # Cache'dan kodni olish
                logger.info(f"Cache stored code: {cache_code}")  # Cache'dagi kodni logga chiqarish

                if cache_code is None:
                    return Response({'message': 'Verification code expired or not found'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if verification_code == cache_code:
                    user, created = User.objects.get_or_create(phone_number=phone_number)
                    if created:
                        user.save()

                    # Generate JWT token for the user
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    })

                return Response({'message': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







    # @action(detail=False, methods=['post'])
    # def verify_sms(self, request):
    #     # So‘rovda yuborilayotgan JSON ma'lumotlarni logga chiqaramiz
    #     logger.info(f"Received verify_sms data: {request.data}")  # Bu ma'lumotlarni loglarda ko‘rish mumkin
    #
    #     serializer = VerifySMSSerializer(data=request.data)
    #     if serializer.is_valid():
    #         phone_number = serializer.validated_data['phone_number']
    #         verification_code = serializer.validated_data['verification_code']
    #         cache_code = cache.get(phone_number)
    #
    #         if verification_code == cache_code:
    #             user, created = User.objects.get_or_create(phone_number=phone_number)
    #             if created:
    #                 user.save()
    #
    #             # Generate JWT token for the user
    #             refresh = RefreshToken.for_user(user)
    #             return Response({
    #                 'refresh': str(refresh),
    #                 'access': str(refresh.access_token)
    #             })
    #
    #         return Response({'message': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






    # @action(detail=False, methods=['post'])
    # def verify_sms(self,request):
    #     serializer = VerifySMSSerializer(data=request.data)
    #     if serializer.is_valid():
    #         phone_number = serializer.validated_data['phone_number']
    #         verification_code = serializer.validated_data['verification_code']
    #         cache_code = cache.get(phone_number)
    #         if verification_code == cache_code:
    #             user, created = User.objects.get_or_create(phone_number=phone_number)
    #             if created:
    #                 # Set other fields like username, email, etc. if needed
    #                 user.save()
    #
    #             # Generate JWT token for the user
    #             refresh = RefreshToken.for_user(user)
    #             return Response({
    #                 'refresh': str('refresh'),
    #                 'access': str('refresh.access_token')
    #             })
    #         return Response({'message': 'Invalid verification code'},status=status.HTTP_400_BAD_REQUEST)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



