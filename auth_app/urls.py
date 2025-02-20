# from django.urls import path,include
# from .views import SMSLoginViewSet
# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register(r'sms_auth', SMSLoginViewSet, basename='sms_auth')
#
# # urlpatterns = [
# #     path('send-sms/', SMSLoginViewSet.as_view({'post': 'send_sms'}), name='send_sms'),
# #     path('verify-sms/', SMSLoginViewSet.as_view({'post': 'verify_sms'}), name='verify_sms'),
# # ]
#
# urlpatterns = [
#     path('', include(router.urls)),  # Router ishlatiladi
# ]

from django.urls import path
from .views import SMSLoginViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', SMSLoginViewSet, basename='sms_auth')  # SMS_AUTH ni olib tashladik

urlpatterns = router.urls + [
    path('send-sms/', SMSLoginViewSet.as_view({'post': 'send_sms'}), name='send_sms'),
    path('verify-sms/', SMSLoginViewSet.as_view({'post': 'verify_sms'}), name='verify_sms'),
]
